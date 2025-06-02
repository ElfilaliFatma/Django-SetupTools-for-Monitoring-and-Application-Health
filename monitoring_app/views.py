from rest_framework import viewsets
from .models import Metric, AlertRule
from .serializers import MetricSerializer, AlertRuleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponse, JsonResponse
from prometheus_client import Gauge, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
import psutil

class MetricViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.all()
    serializer_class = AlertRuleSerializer

@csrf_exempt  
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_metric_api(request):
    cpu_percent = psutil.cpu_percent(interval=1)
    metric, _ = Metric.objects.get_or_create(
        name="cpu_usage",
        defaults={
            "description": "CPU usage percentage",
            "value": cpu_percent,
            "instance": "localhost:8000",
            "job": "django"
        }
    )
    metric.value = cpu_percent
    metric.save()
    return JsonResponse({'status': 'ok', 'cpu': cpu_percent})
import random

def metrics_view(request):
    registry = CollectorRegistry()
    cpu = Gauge('cpu_usage', 'CPU usage in percent', registry=registry)
    cpu.set(10 + random.random() * 30)  


    for m in Metric.objects.all():
        try:
            g = Gauge(m.name, m.description or "", registry=registry)
            g.set(m.value)
        except ValueError:
            continue

    return HttpResponse(generate_latest(registry), content_type=CONTENT_TYPE_LATEST)
