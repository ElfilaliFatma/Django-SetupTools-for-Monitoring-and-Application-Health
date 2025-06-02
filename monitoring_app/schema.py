import graphene
from graphene_django import DjangoObjectType
from django.db import models
from graphql import GraphQLError 
from .models import Metric, AlertRule


class MetricType(DjangoObjectType):
    class Meta:
        model = Metric
        fields = '__all__'

class AlertRuleType(DjangoObjectType):
    class Meta:
        model = AlertRule
        fields = '__all__'

class DashboardSummaryType(graphene.ObjectType):
    total_metrics = graphene.Int()
    total_alert_rules = graphene.Int()
    active_alert_rules = graphene.Int()
    metrics_exceeding_warning = graphene.List(MetricType)
    metrics_exceeding_critical = graphene.List(MetricType)


class Query(graphene.ObjectType):
    all_metrics = graphene.List(MetricType)
    all_alert_rules = graphene.List(AlertRuleType)
    dashboard_summary = graphene.Field(DashboardSummaryType)

    def resolve_all_metrics(root, info):
        return Metric.objects.all()

    def resolve_all_alert_rules(root, info):
        return AlertRule.objects.all()

    def resolve_dashboard_summary(root, info):
        total_metrics = Metric.objects.count()
        total_alert_rules = AlertRule.objects.count()
        active_alert_rules = AlertRule.objects.filter(is_active=True).count()

        warning_metric_ids = AlertRule.objects.filter(
            is_active=True,
            warning_threshold__lte=models.F('metric__current_value'),
            critical_threshold__gt=models.F('metric__current_value')
        ).values_list('metric_id', flat=True)

        critical_metric_ids = AlertRule.objects.filter(
            is_active=True,
            critical_threshold__lte=models.F('metric__current_value')
        ).values_list('metric_id', flat=True)

        metrics_exceeding_warning = Metric.objects.filter(id__in=warning_metric_ids)
        metrics_exceeding_critical = Metric.objects.filter(id__in=critical_metric_ids)

        return DashboardSummaryType(
            total_metrics=total_metrics,
            total_alert_rules=total_alert_rules,
            active_alert_rules=active_alert_rules,
            metrics_exceeding_warning=metrics_exceeding_warning,
            metrics_exceeding_critical=metrics_exceeding_critical,
        )


class CreateMetric(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        value = graphene.Float(required=True) 

    metric = graphene.Field(MetricType)

    def mutate(root, info, name, value):
        if value < 0:
            raise GraphQLError("Metric value cannot be negative.")
        metric = Metric.objects.create(name=name, value=value)
        return CreateMetric(metric=metric)
    
class UpdateMetric(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        value = graphene.Float(required=True)

    metric = graphene.Field(MetricType)

    def mutate(root, info, id, value):
        if value < 0:
            raise GraphQLError("Metric value cannot be negative.")
        try:
            metric = Metric.objects.get(pk=id)
        except Metric.DoesNotExist:
            raise GraphQLError(f"Metric with id {id} does not exist.")
        metric.value = value
        metric.save()
        return UpdateMetric(metric=metric)

class CreateAlertRule(graphene.Mutation):
    class Arguments:
        metric_id = graphene.ID(required=True)
        warning_threshold = graphene.Float(required=True)
        critical_threshold = graphene.Float(required=True)
        is_active = graphene.Boolean(required=True)

    alert_rule = graphene.Field(AlertRuleType)

    def mutate(root, info, metric_id, warning_threshold, critical_threshold, is_active):
        if warning_threshold < 0 or critical_threshold < 0:
            raise GraphQLError("Threshold values cannot be negative.")
        if critical_threshold <= warning_threshold:
            raise GraphQLError("Critical threshold must be greater than warning threshold.")
        try:
            metric = Metric.objects.get(pk=metric_id)
        except Metric.DoesNotExist:
            raise GraphQLError(f"Metric with id {metric_id} does not exist.")
        alert_rule = AlertRule.objects.create(
            metric=metric,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            is_active=is_active
        )
        return CreateAlertRule(alert_rule=alert_rule)

class Mutation(graphene.ObjectType):
    create_metric = CreateMetric.Field()
    create_alert_rule = CreateAlertRule.Field()
    update_metric = UpdateMetric.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)



from .models import MetricValue  

class UpdateMetric(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        value = graphene.Float(required=True)

    metric = graphene.Field(MetricType)

    def mutate(root, info, id, value):
        metric = Metric.objects.get(pk=id)
        metric.value = value
        metric.save()
      
        MetricValue.objects.create(metric=metric, value=value)
        return UpdateMetric(metric=metric)

