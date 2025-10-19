# 🎯 Talent Mosaic - Django Edition

Sistema completo di talent management basato su Python/Django.

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
