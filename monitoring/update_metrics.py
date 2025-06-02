from celery import shared_task
import psutil
from monitoring_app.models import Metric

@shared_task
def update_cpu_usage_task():
    cpu_percent = psutil.cpu_percent(interval=1)
    metric, created = Metric.objects.get_or_create(
        name="cpu_usage",
        defaults={"description": "CPU usage in percent"}
    )
    metric.value = cpu_percent
    metric.save()
