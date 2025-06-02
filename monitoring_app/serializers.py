from rest_framework import serializers
from .models import Metric, AlertRule

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['name','description','value','current_value',]

class AlertRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRule
        fields = '__all__'

    def validate(self, data):
        if data['warning_threshold'] >= data['critical_threshold']:
            raise serializers.ValidationError("Warning threshold must be less than critical threshold.")
        return data
