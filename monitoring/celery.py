import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring.settings')

app = Celery('monitoring')
app.config_from_object('django.conf:settings', namespace='CELERY')

# autodiscover all tasks.py in installed apps
app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    'scrape_metrics': {
        'task': 'monitoring_app.tasks.scrape_prometheus_metrics',
        'schedule': 10.0,  
    },
    'check_anomalies': {
        'task': 'monitoring_app.tasks.check_metric_anomalies',
        'schedule': 15.0,
    },
}

