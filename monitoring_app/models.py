from django.db import models
from django.core.exceptions import ValidationError

class Metric(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    value = models.FloatField()
    current_value = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    job = models.CharField(max_length=100, default="django")
    instance = models.CharField(max_length=100, default="localhost:8000")
    prometheus_query = models.CharField(max_length=255, help_text="The PromQL query to fetch this metric")


    def __str__(self):
        return self.name

    @classmethod
    def create_or_update_metric(cls, name, description='', value=0, current_value=None, unit=''):
        metric, created = cls.objects.update_or_create(
            name=name,
            defaults={
                'description': description,
                'value': value,
                'current_value': current_value,
                'unit': unit,
                'instance': 'localhost:8000',
                'job': 'django',
            }
        )
        return metric, created

class AlertRule(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='alert_rules')
    warning_threshold = models.FloatField()
    critical_threshold = models.FloatField()
    notify_email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.warning_threshold >= self.critical_threshold:
            raise ValidationError("Warning threshold must be less than critical threshold.")

    def __str__(self):
        return f"Alert for {self.metric.name} (W:{self.warning_threshold} / C:{self.critical_threshold})"

class MetricValue(models.Model):
    metric = models.ForeignKey('Metric', on_delete=models.CASCADE, related_name='values')
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
   

    def __str__(self):
        return f"{self.metric.name} at {self.timestamp}: {self.value}"