from django.http import HttpResponse
from prometheus_client import Gauge, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
from .models import Metric

def metrics_view(request):
    registry = CollectorRegistry()

    # Add static CPU metric (for testing, remove if using psutil)
    cpu = Gauge('cpu_usage', 'CPU usage in percent', registry=registry)
    # cpu.set(95.0)  # Replace with real CPU usage from psutil or DB

    # Add metrics from DB
    for m in Metric.objects.all():
        try:
            g = Gauge(m.name, m.description or "", registry=registry)
            g.set(m.value)
        except ValueError:
            continue

    return HttpResponse(generate_latest(registry), content_type=CONTENT_TYPE_LATEST)
