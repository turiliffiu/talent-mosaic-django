# 🚀 GUIDA RAPIDA - Script Installazione Automatica Dashboard

## 📋 Prerequisiti

- Server Ubuntu 20.04 / 22.04 / 24.04
- Accesso root o sudo
- Connessione Internet

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

---

## 🎯 INSTALLAZIONE IN 3 PASSI

### 1️⃣ Scarica lo script

```bash
wget https://raw.githubusercontent.com/turiliffiu/talent-mosaic-django/main/install.sh
```

### 2️⃣ Rendi eseguibile

```bash
chmod +x install.sh
```

### 3️⃣ Esegui come root

```bash
sudo bash install.sh
```

---

## 🔄 COSA FA LO SCRIPT

Lo script esegue automaticamente tutti i passaggi del README:

### ✅ STEP 1: Verifica Sistema
- Controlla che sei root
- Rileva automaticamente l'IP del server
- Ti chiede conferma prima di procedere

### ✅ STEP 2: Aggiornamento Sistema
- `apt update`
- `apt upgrade -y`

### ✅ STEP 3: Installazione Pacchetti
- Python 3.11
- Nginx
- Redis
- Supervisor
- Git

### ✅ STEP 4: Creazione Utente
- Crea utente `talent`
- Configura home in `/opt/talent`

### ✅ STEP 5: Clonazione Progetto
- Clona da GitHub automaticamente

### ✅ STEP 6: Ambiente Virtuale
- Crea virtual environment
- Installa tutte le dipendenze Python
- Installa Gunicorn

### ✅ STEP 7: Configurazione Django
- **Genera automaticamente SECRET_KEY sicura**
- Crea file `.env` con configurazioni corrette
- Esegue `migrate`
- Esegue `collectstatic`
- Ti chiede se vuoi creare superuser
- Popola database con esempi

### ✅ STEP 8: Permessi (FONDAMENTALE!)
- Imposta `chmod 755` su `/opt` e `/opt/talent`
- Imposta `chmod -R 755` su `staticfiles`
- **Verifica** che `www-data` possa leggere i file

### ✅ STEP 9: Configurazione Nginx
- Crea configurazione con IP rilevato automaticamente
- Attiva il sito
- Disattiva sito default
- Testa configurazione con `nginx -t`
- Riavvia Nginx

### ✅ STEP 10: Systemd (Gunicorn)
- Crea service systemd
- Avvia Gunicorn automaticamente
- Abilita autostart al boot

### ✅ STEP 11: Verifica Finale
- Controlla che tutti i servizi siano attivi
- Testa accesso ai file statici
- Mostra riepilogo con URL e comandi utili

---

## 🎬 ESEMPIO OUTPUT

```
═══════════════════════════════════════════════════════
STEP 1: VERIFICA SISTEMA E RACCOLTA INFORMAZIONI
═══════════════════════════════════════════════════════

✅ Eseguito come root
ℹ️  IP rilevato: 192.168.1.188

L'IP del server è corretto? (s per confermare, n per modificare)
s
✅ IP server impostato: 192.168.1.188
...
```

---

## 📝 DOPO L'INSTALLAZIONE

### Accedi alla Dashboard
```
http://TUO_IP_SERVER
```

### Crea Superuser (se non fatto durante installazione)
```bash
sudo su - talent
cd /opt/talent
source venv/bin/activate
python manage.py createsuperuser
```

### Accedi all'Admin
```bash
http://TUO_IP_SERVER/admin
```

---

## 🔧 COMANDI UTILI

### Riavvia Servizi
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Visualizza Log
```bash
# Log Gunicorn in tempo reale
sudo journalctl -u gunicorn -f

# Log Nginx errori
sudo tail -f /var/log/nginx/talent_error.log

# Log Nginx accessi
sudo tail -f /var/log/nginx/talent_access.log
```

### Status Servizi
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status redis-server
```

### Aggiorna Progetto
```bash
sudo su - talent
cd /opt/talent
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
exit

# Riavvia Gunicorn
sudo systemctl restart gunicorn
```

---

## 🛠️ RISOLUZIONE PROBLEMI

### Problema: Script si interrompe

**Causa:** Errore in uno step precedente

**Soluzione:**
```bash
# Visualizza errore specifico
# Lo script mostra sempre cosa è andato storto

# Puoi rieseguire lo script
sudo bash install.sh
# Lo script rileverà cosa è già installato e continuerà
```

### Problema: Gunicorn non parte

**Verifica log:**
```bash
sudo journalctl -u gunicorn -n 50
```

**Possibili cause:**
- File `.env` mancante o errato
- Virtual environment non creato correttamente
- Porta 8000 già in uso

### Problema: 403 Forbidden sui file statici

**Verifica permessi:**
```bash
ls -la /opt/dashboard/staticfiles/css/
sudo -u www-data cat /opt/dashboard/staticfiles/css/style.css
```

**Correggi manualmente:**
```bash
sudo chmod 755 /opt
sudo chmod 755 /opt/talent
sudo chmod -R 755 /opt/talent/staticfiles
sudo systemctl restart nginx
```

### Problema: Nginx non parte

**Test configurazione:**
```bash
sudo nginx -t
```

**Visualizza errori:**
```bash
sudo tail -f /var/log/nginx/error.log
```

---

## 🔒 SICUREZZA

### File .env

Lo script genera automaticamente una SECRET_KEY sicura, ma verifica sempre:

```bash
sudo cat /opt/talent/.env
```

Dovrebbe contenere:
```
DEBUG=False
SECRET_KEY=una_chiave_lunga_e_casuale_generata_automaticamente
STATIC_ROOT=/opt/talent/staticfiles
STATIC_URL=/static/
```

### Permessi File Sensibili

```bash
# .env deve essere leggibile solo da dashboard
sudo chmod 600 /opt/talent/.env
sudo chown talent:talent /opt/talent/.env

# Database deve essere protetto
sudo chmod 600 /opt/talent/db.sqlite3
sudo chown talent:talent /opt/talent/db.sqlite3
```

---

## 📊 STRUTTURA FILE DOPO INSTALLAZIONE

```
talent-mosaic-django/
│
├── 📁 talent_mosaic/           # ⚙️ App principale Django (configurazione)
│   ├── __init__.py
│   ├── asgi.py                 # ASGI config per deploy asincrono
│   ├── celery.py               # Configurazione Celery task queue
│   ├── settings.py             # ⚙️ Configurazioni Django principali
│   ├── urls.py                 # 🔗 URL routing principale
│   └── wsgi.py                 # WSGI config per deploy produzione
│
├── 📁 accounts/                # 👤 Gestione utenti e profili
│   ├── __init__.py
│   ├── admin.py                # Configurazione admin Django
│   ├── apps.py                 # Configurazione app
│   ├── forms.py                # Form registrazione/login
│   ├── models.py               # 📊 UserProfile model
│   ├── urls.py                 # URL login/register/profile
│   └── views.py                # View autenticazione
│
├── 📁 skills/                  # 🎯 Gestione competenze
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                # Form aggiunta competenze
│   ├── models.py               # 📊 Skill, SkillCategory, UserSkill
│   ├── urls.py
│   └── views.py                # Lista/aggiungi/modifica skill
│
├── 📁 matching/                # 🤝 Sistema matchmaking
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   └── views.py                # Algoritmo matching basato su skill
│
├── 📁 mentorship/              # 👥 Programmi mentoring
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # 📊 Mentorship, MentorshipSession
│   ├── urls.py
│   └── views.py                # Gestione relazioni mentor-mentee
│
├── 📁 events/                  # 📅 Eventi e workshop
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # 📊 Event, EventRegistration
│   ├── urls.py
│   └── views.py                # Lista eventi, registrazione
│
├── 📁 challenges/              # 🏆 Challenge collaborative
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # 📊 Challenge, ChallengeParticipation
│   ├── urls.py
│   └── views.py                # Gestione challenge e partecipazione
│
├── 📁 badges/                  # 🏅 Sistema badge e riconoscimenti
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # 📊 Badge, UserBadge
│   ├── urls.py
│   └── views.py                # Assegnazione e visualizzazione badge
│
├── 📁 analytics/               # 📊 Analytics e metriche
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Modelli per tracking
│   ├── urls.py
│   └── views.py                # Dashboard analytics
│
├── 📁 core/                    # 🏠 Pagine core (home, about)
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   └── views.py                # Home, dashboard, about
│
├── 📁 api/                     # 🔌 REST API
│   ├── __init__.py
│   ├── apps.py
│   └── urls.py                 # Endpoint API (DRF)
│
├── 📁 templates/               # 🎨 Template HTML
│   ├── base.html               # Template base con navbar
│   ├── 404.html                # Pagina errore 404
│   ├── 500.html                # Pagina errore 500
│   │
│   ├── 📁 accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── profile_edit.html
│   │
│   ├── 📁 skills/
│   │   ├── my_skills.html
│   │   └── skill_list.html
│   │
│   ├── 📁 events/
│   │   └── event_list.html
│   │
│   ├── 📁 challenges/
│   │   └── challenge_list.html
│   │
│   ├── 📁 badges/
│   │   ├── badge_list.html
│   │   └── my_badges.html
│   │
│   ├── 📁 mentorship/
│   │   └── mentorship_list.html
│   │
│   ├── 📁 matching/
│   │   └── matches.html
│   │
│   ├── 📁 analytics/
│   │   └── dashboard.html
│   │
│   └── 📁 core/
│       ├── home.html
│       ├── dashboard.html
│       └── about.html
│
├── 📁 static/                  # 📦 File statici (CSS, JS, immagini)
│   └── 📁 css/
│       └── style.css           # CSS personalizzato
│
├── 📁 scripts/                 # 🛠️ Script utility
│   ├── backup.sh               # Script backup database
│   ├── deploy.sh               # Script deploy
│   └── seed_data.py            # Popolamento database test
│
├── 📄 manage.py                # 🐍 Django management script
├── 📄 requirements.txt         # 📦 Dipendenze Python
├── 📄 gunicorn_config.py       # ⚙️ Configurazione Gunicorn
│
├── 📄 README.md                # 📖 Documentazione principale
├── 📄 SCRIPTS_README.md        # 📖 Documentazione script
│
├── 🔧 activate.sh              # Script attivazione Linux/Mac
├── 🔧 activate.bat             # Script attivazione Windows
├── 🔧 setup.py                 # Script setup automatico
├── 🔧 manage_production.sh     # Script gestione produzione
└── 🔧 Makefile                 # Comandi make rapidi
```

---

## ⚙️ PERSONALIZZAZIONE SCRIPT

### Cambia Porta Gunicorn

Modifica nello script:
```bash
# Cerca questa riga:
--bind 127.0.0.1:8000 \\

# Cambia in:
--bind 127.0.0.1:9000 \\
```

Poi aggiorna anche Nginx:
```bash
# Nel blocco upstream:
upstream talent {
    server 127.0.0.1:9000 fail_timeout=0;
}
```

### Cambia Repository GitHub

Modifica all'inizio dello script:
```bash
GIT_REPO="https://github.com/TUO_USERNAME/TUO_REPO.git"
```

### Cambia Percorso Installazione

Modifica:
```bash
PROJECT_PATH="/tuo/percorso/personalizzato"
```

---

## 🎓 NOTE AVANZATE

### Modalità Non Interattiva

Se vuoi eseguire lo script senza prompt interattivi:

```bash
# Salta la creazione superuser
# Conferma automaticamente tutti i prompt
yes | sudo bash install.sh
```

### Installazione Multi-Server

Lo script può essere usato su più server:
1. Ogni server avrà il proprio database SQLite
2. Ogni server rileverà automaticamente il proprio IP
3. Per database condiviso, configura PostgreSQL manualmente

### Backup Prima dell'Installazione

```bash
# Backup directory se già esiste
sudo tar -czf /root/talent_backup_$(date +%Y%m%d_%H%M%S).tar.gz /opt/talent

# Backup database
sudo cp /opt/talent/db.sqlite3 /root/db_backup_$(date +%Y%m%d).sqlite3
```

---

## 📞 SUPPORTO

Se hai problemi con lo script:

1. **Leggi i messaggi di errore** - Lo script mostra sempre cosa va storto
2. **Controlla i log** - Gunicorn e Nginx hanno log dettagliati
3. **Verifica prerequisiti** - Ubuntu compatibile, accesso root, internet
4. **Riesegui lo script** - È idempotente (può essere eseguito più volte)

---

## ✅ CHECKLIST POST-INSTALLAZIONE

- [ ] Dashboard accessibile da browser
- [ ] CSS caricano correttamente
- [ ] Login funziona
- [ ] Superuser creato
- [ ] Admin accessibile
- [ ] File di esempio caricati
- [ ] Gunicorn si riavvia automaticamente
- [ ] Nginx serve i file statici
- [ ] Nessun errore nei log

---

**🎉 Buon utilizzo della Dashboard!**
