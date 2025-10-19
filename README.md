# 🎯 Talent Mosaic - Django Edition

Talent Mosaic è un programma innovativo che mira a valorizzare le persone e le loro competenze, promuovendo una cultura aziendale realmente inclusiva, collaborativa e orientata alla crescita.
Attraverso una piattaforma digitale interna, l’iniziativa permette a ogni dipendente di esprimere il proprio potenziale, condividere esperienze e sviluppare nuove connessioni professionali, favorendo così l’incontro tra diversità e innovazione.

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
