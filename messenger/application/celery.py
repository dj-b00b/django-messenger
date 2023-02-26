import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

app = Celery('application')

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {  
    "backup": {
        "task": "chats.tasks.backup_db",
        "schedule": crontab(hour=4, minute=30)   # Everyday at 04:30
    },
}