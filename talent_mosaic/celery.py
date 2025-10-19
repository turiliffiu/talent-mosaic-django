import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talent_mosaic.settings')

app = Celery('talent_mosaic')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-daily-digest': {
        'task': 'analytics.tasks.send_daily_digest',
        'schedule': crontab(hour=8, minute=0),
    },
}
