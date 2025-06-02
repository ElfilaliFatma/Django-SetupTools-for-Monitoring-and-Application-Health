from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MetricViewSet, AlertRuleViewSet, metrics_view, update_metric_api
from django_prometheus import exports

router = DefaultRouter()
router.register(r'metrics', MetricViewSet)
router.register(r'alert-rules', AlertRuleViewSet, basename='alert-rule')

urlpatterns = [
    path('', include(router.urls)),  
    path('prometheus-metrics/', exports.ExportToDjangoView), 
    path('update-cpu/', update_metric_api, name='update_cpu'),
    path('met/', metrics_view, name='metrics_view'), 
    path('addmet/', metrics_view, name='metrics_view'), 
    path('metrics/', MetricViewSet.as_view({'get': 'list'}), name='metrics'),
]+ router.urls
