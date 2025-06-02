import requests
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from .models import AlertRule, Metric, MetricValue
import psutil


from monitoring_app.ml_model import detect_anomalies_with_ai

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

@shared_task
def scrape_prometheus_metrics():
    print("Running scrape_prometheus_metrics()...")
    for metric in Metric.objects.all():
        print(f"Querying Prometheus for: {metric.prometheus_query}")
        try:
            response = requests.get(PROMETHEUS_URL, params={"query": metric.prometheus_query})
            response_json = response.json()
            print("Prometheus response:", response_json)

            data = response_json.get("data", {})
            result_type = data.get("resultType")

            if result_type == "scalar":
                timestamp, value = data.get("result", [None, None])
                if value is not None:
                    MetricValue.objects.create(
                        metric=metric,
                        value=float(value),
                        timestamp=timezone.now()
                    )
                    metric.value = float(value)
                    metric.save()
                    print(f"Saved scalar value {value} for metric {metric.name}")

            elif result_type == "vector":
                last_value = None
                for result in data.get("result", []):
                    value = float(result["value"][1])
                    MetricValue.objects.create(
                        metric=metric,
                        value=value,
                        timestamp=timezone.now()
                    )
                    last_value = value
                    print(f"Saved vector value {value} for metric {metric.name}")
                if last_value is not None:
                    metric.value = last_value
                    metric.save()

            else:
                print(f"Unsupported result type: {result_type}")

        except Exception as e:
            print("Error during scraping:", e)


@shared_task
def check_metric_anomalies():
    print("Starting anomaly check...")
    metrics = Metric.objects.all()

    for metric in metrics:
        values = list(
            MetricValue.objects
            .filter(metric=metric)
            .order_by('-timestamp')
            .values_list('value', flat=True)[:50]
        )
        values.reverse()  

        if len(values) < 10:
            print(f"Not enough data for {metric.name}")
            continue

        if detect_anomalies_with_ai(values):
            print(f"🚨 AI detected anomaly in metric: {metric.name}")
           
        else:
            print(f"No anomaly in metric: {metric.name}")

    print("Finished anomaly check.")


@shared_task
def update_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    Metric.objects.update_or_create(
        name="cpu_usage",
        defaults={
            "description": "CPU usage percentage",
            "value": cpu_percent,
            "instance": "localhost:8000",
            "job": "django"
        }
    )
