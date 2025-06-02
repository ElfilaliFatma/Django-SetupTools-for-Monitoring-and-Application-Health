from monitoring_app.models import MetricValue, Metric
from django.utils.timezone import now
import datetime

metric, created = Metric.objects.get_or_create(name='up')
base_time = now()

for i in range(20):
    MetricValue.objects.create(
        metric=metric,
        value=1.0 + 0.05 * i,
        timestamp=base_time - datetime.timedelta(minutes=(20 - i))
    )
