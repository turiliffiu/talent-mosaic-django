# 🎯 Talent Mosaic - Django Edition

Talent Mosaic è un programma innovativo che mira a valorizzare le persone e le loro competenze, promuovendo una cultura aziendale realmente inclusiva, collaborativa e orientata alla crescita.
Attraverso una piattaforma digitale interna, l’iniziativa permette a ogni dipendente di esprimere il proprio potenziale, condividere esperienze e sviluppare nuove connessioni professionali, favorendo così l’incontro tra diversità e innovazione.

## Obiettivi principali

- Creare un ambiente di lavoro più equo e rappresentativo, in cui tutti possano sentirsi valorizzati.

- Favorire la collaborazione tra persone di età, esperienze e background differenti.

- Dare visibilità ai talenti “nascosti” e alle competenze trasversali già presenti in azienda.

- Stimolare la crescita professionale e lo sviluppo continuo attraverso percorsi di mentoring.

- Promuovere l’inclusione come motore di innovazione organizzativa.

## Descrizione del funzionamento dell’applicativo informatico

L’applicativo Talent Mosaic è una piattaforma integrata accessibile da web e mobile.
Ogni dipendente dispone di un profilo personale che racchiude competenze tecniche, soft skills, passioni e disponibilità a partecipare a programmi di mentoring o progetti cross-team.
Un motore di matchmaking basato su intelligenza artificiale suggerisce connessioni, team di progetto e opportunità di collaborazione, facilitando la creazione di una rete di conoscenze interne.

La piattaforma include anche:

- Programmi di Mentorship e Reverse Mentoring, per favorire il dialogo intergenerazionale e la condivisione di competenze.

- Laboratori di Inclusione e Storytelling, per promuovere ascolto, empatia e confronto.

- Challenge sulla diversità, dove team eterogenei lavorano insieme su idee innovative.

- Sistema di badge peer-to-peer, che riconosce e valorizza comportamenti inclusivi e collaborativi.

## Benefici attesi

- Inclusione concreta: ogni persona valorizzata per ciò che porta di unico.

- Crescita professionale diffusa: sviluppo continuo delle competenze interne.

- Cultura collaborativa: differenze trasformate in valore aggiunto.

- Innovazione sociale e organizzativa: nuove idee nate dall’incontro tra prospettive diverse.

- Rafforzamento dell’identità aziendale: FiberCop come azienda che cresce attraverso le persone.


## Requisiti

- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Proxmox VE 8+ (per deployment)

## Installazione Rapida
## 🪟 1️⃣ — Preparare il server su Proxmox
### Crea un Container Ubuntu:
     
      - arch: amd64
      - cores: 1
      - features: nesting=1
      - hostname: dashboard
      - memory: 2048
      - net0: name=eth0,bridge=vmbr0,firewall=1,ip=dhcp
      - ostype: ubuntu
      - rootfs: local-lvm,size=20G
      - swap: 2048
      - unprivileged: 1

Sulla shell del nuovo Container su Proxmox:

```bash
sudo nano /etc/ssh/sshd_config
```

Modificare i seguenti parametri:

```bash
PermitRootLogin yes
PasswordAuthentication yes
PermitEmptyPasswords no
```

Installare ifconfig

```bash
apt update
apt install -y net-tools 
```
          
## 🧰 2️⃣ — Installare i pacchetti necessari
### SSH nella VM
`ssh root@192.168.1.xxx` <br>

### 1. Aggiorna sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Installa Python 3.11
```bash
sudo apt install python3.11 python3.11-venv python3.11-dev -y
sudo apt install python3-pip build-essential libpq-dev -y
```
### 3. Installa NGINX
```bash
sudo apt install nginx -y
sudo systemctl enable nginx
```

### 4. Installa Redis
```bash
sudo apt install redis-server -y
sudo systemctl enable redis-server
```

### 5. Installa supervisor (per gestire processi)
```bash
sudo apt install supervisor -y
sudo systemctl enable supervisor
```

### 6. Installa Git
```bash
sudo apt install git -y
```

### 7. Installa Curl
```bash
apt install -y curl
```

### 8. Crea utente applicativo
```bash
sudo adduser --system --group --home /opt/talent talent
sudo mkdir -p /opt/talent
sudo chown talent:talent /opt/talent
```

## 🧬 3️⃣ — Clonare il progetto da GitHub
### 1. Diventa utente talent
```bash
sudo usermod -s /bin/bash talent
sudo su - talent
```

### 2. Clona repository
```bash
cd /opt/talent
```

```bash
git clone https://github.com/turiliffiu/talent-mosaic-django.git .
```

Ora la struttura del progetto Django sarà disponibile sul server

## 🐍 4️⃣ — Creare l'ambiente virtuale e installare le dipendenze
### 1. Crea virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 2. Installa dipendenze
```bash
pip install --upgrade pip
pip install -r requirements.txt
```


## ⚙️ 5️⃣ — Configurare Django
### Crea il file `.env`

```bash
nano .env
```

Scrivi:

```bash
DEBUG=False
SECRET_KEY=metti_una_tua_chiave_sicura    
STATIC_ROOT=/opt/talent/staticfiles
STATIC_URL=/static/
```


### Esegui le migrazioni e raccogli statici
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

NOTA: il superuser serve per entrare nell'appweb come amministratore quindi, se si vuole, si può usare come nome `admin`

### Popola il data base con dei file di esempio
```bash
python manage.py populate_db
 ```

### Testa il server Django (verifica che funzioni)

ATTENZIONE: per testare in server in locale devi impostare `DEBUG=True` sul file `.env`
```bash
python manage.py runserver 0.0.0.0:8000
```

Apri il browser e vai su:

```bash
http://IP_del_server:8000
```

Se vedi il tuo sito Django → funziona!

ATTENZIONE: per continuare con il server in deploy devi impostare `DEBUG=False` sul file `.env`

## 🔥 6️⃣ — Esegui con Gunicorn

Interrompi il server di sviluppo (CTRL+C) e installa Gunicorn:

```bash
pip install gunicorn
```

Prova a eseguire l'app:

```bash
gunicorn --bind 0.0.0.0:8000 talent_mosaic.wsgi
```

(sostituisci nome_progetto con quello della tua cartella Django principale — quella dove c'è settings.py)

## 🌐 7️⃣ — Configura Nginx come reverse proxy

Crea un file di configurazione da utente `root`:

```bash
nano /etc/nginx/sites-available/talent
```

Inserisci:

     upstream talent {
         server 127.0.0.1:8000 fail_timeout=0;
     }
     
     server {
         listen 80;
         server_name 192.168.1.xxx talent.local;  # Sostituisci xxx con il tuo IP
         
         client_max_body_size 10M;
         
         # File statici (CSS, JS, immagini)
         location /static/ {
             alias /opt/talent/staticfiles/;
             expires 30d;
             add_header Cache-Control "public, immutable";
         }
         
         # Tutte le altre richieste vanno a Gunicorn
         location / {
             proxy_pass http://talent;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header Host $host;
             proxy_set_header X-Forwarded-Proto $scheme;
             proxy_redirect off;
             
             # Timeout per richieste lunghe
             proxy_connect_timeout 300;
             proxy_send_timeout 300;
             proxy_read_timeout 300;
         }
         
         # Log
         access_log /var/log/nginx/talent_access.log;
         error_log /var/log/nginx/talent_error.log;
     }

ATTENZIONE: assicurati che NON ci siano spazi all'inizio di ogni riga quando fai copia/incolla. Le righe devono iniziare senza spazi a sinistra.

## 🔐 7.5️⃣ — CONFIGURA I PERMESSI (FONDAMENTALE!)

**IMPORTANTE:** Questo passaggio è **CRITICO** per evitare errori 403 Forbidden sui file statici!

Esegui i seguenti comandi come utente `root`:

### 1. Permessi sulle directory parent
```bash
chmod 755 /opt
chmod 755 /opt/talent
```

**Perché è necessario?** Nginx (utente `www-data`) deve poter "attraversare" tutte le directory fino ad arrivare ai file CSS/JS.

### 2. Permessi sui file statici
```bash
chmod -R 755 /opt/talent/staticfiles
chown -R talent:talent /opt/talent/staticfiles
```

### 3. Verifica che www-data possa leggere i file
```bash
sudo -u www-data cat /opt/talent/staticfiles/css/style.css | head -5
```

Se vedi il contenuto del CSS, i permessi sono corretti! ✅

Se ottieni "Permission denied", ripeti i comandi chmod sopra.

### 4. Attiva la configurazione Nginx
```bash
ln -s /etc/nginx/sites-available/talent /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
systemctl status nginx
```

### 5. Test accesso diretto al CSS
Apri nel browser:
```bash
http://IP_del_server/static/css/style.css
```

**Dovresti vedere il contenuto del file CSS.** Se ottieni 403 o 404, rivedi i permessi!

Torna all'utente talent:

```bash
sudo su - talent
```
```bash
cd /opt/talent
```
```bash
source venv/bin/activate 
```

Avvia Gunicorn:

```bash
gunicorn --bind 127.0.0.1:8000 --workers 3 talent_mosaic.wsgi:application
```

Controlla se funziona aprendo:

`http://IP_del_server`


Dovresti vedere la tua app Django servita tramite Nginx ✅

## ⚙️ 8️⃣ — Automatizzazione Gunicorn con systemd

### Passi per configurare:
Crea la directory per i log (come root):

```bash
mkdir -p /var/log/talent
chown talent:talent /var/log/talent
```

Crea il file systemd (come root):

```bash
nano /etc/systemd/system/gunicorn.service
```

Incolla questa configurazione:

     [Unit]
     Description=Gunicorn daemon for Dashboard Django project
     After=network.target
     
     [Service]
     Type=notify
     User=talent
     Group=talent
     WorkingDirectory=/opt/talent
     Environment="PATH=/opt/talent/venv/bin"
     ExecStart=/opt/talent/venv/bin/gunicorn \
               --workers 3 \
               --bind 127.0.0.1:8000 \
               --access-logfile /var/log/talent/access.log \
               --error-logfile /var/log/talent/error.log \
               talent_mosaic.wsgi:application
     
     Restart=on-failure
     RestartSec=5s
     
     [Install]
     WantedBy=multi-user.target

ATTENZIONE: togliere gli spazi a sx quando si fa il copia e incolla

Ricarica systemd e avvia il servizio:

```bash
systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn
```

Verifica lo stato:

```bash
systemctl status gunicorn
```

## Ora Gunicorn partirà automaticamente all'avvio del server! 🎉

---

## 🔧 RISOLUZIONE PROBLEMI

### Problema: Errore 403 Forbidden sui file statici

**Sintomo:** La dashboard non carica i CSS, ottieni errore 403.

**Soluzione:**
1. Verifica permessi: `ls -la /opt/dashboard/staticfiles/css/`
2. Esegui: `chmod 755 /opt && chmod 755 /opt/dashboard && chmod -R 755 /opt/dashboard/staticfiles`
3. Testa: `sudo -u www-data cat /opt/dashboard/staticfiles/css/dashboard.css`
4. Riavvia Nginx: `systemctl restart nginx`

### Problema: CSS non si carica nella dashboard

**Verifica:**
1. File .env contiene `STATIC_URL=/static/` (con `/` finale!)
2. Hai eseguito `python manage.py collectstatic`
3. Nginx è configurato correttamente (senza spazi iniziali nelle righe)
4. I permessi sono corretti (vedi sezione 7.5)

### Problema: Gunicorn non si avvia

**Verifica:**
1. `systemctl status gunicorn` per vedere errori
2. Log: `tail -f /var/log/dashboard/error.log`
3. File .env esiste e contiene SECRET_KEY
4. Virtual environment è attivo

---

## 📝 NOTE IMPORTANTI

- ⚠️ **STATIC_URL** nel file .env deve terminare con `/` → `/static/`
- ⚠️ **Permessi 755** sono necessari su `/opt`, `/opt/dashboard` e `staticfiles/`
- ⚠️ La configurazione Nginx **NON deve avere spazi** all'inizio delle righe
- ⚠️ Dopo ogni modifica a `.env`, riavvia Gunicorn: `systemctl restart gunicorn`
- ⚠️ In produzione, **DEBUG deve essere False**

