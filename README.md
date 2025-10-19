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
```bash
# Clone repository
git clone <repo-url>
cd talent-mosaic-django

# Virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Configura .env
cp .env.example .env
nano .env

# Migrazioni
python manage.py migrate

# Crea superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## License

Proprietario - Tutti i diritti riservati
