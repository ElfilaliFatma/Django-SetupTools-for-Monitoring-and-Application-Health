# admin.py
from django.contrib import admin
from .models import Metric,AlertRule,MetricValue


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_latest_value','value')

    def get_latest_value(self, obj):
        latest = MetricValue.objects.filter(metric=obj).order_by('-timestamp').first()
        return latest.value if latest else '-'
    get_latest_value.short_description = 'Current value'


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ['metric', 'warning_threshold', 'critical_threshold', 'notify_email', 'is_active']
