from django.contrib import admin
from django.urls import include, path
from graphene_django.views import GraphQLView
from django_prometheus import exports
from monitoring_app.views import MetricViewSet, metrics_view, update_metric_api
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('monitoring_app.urls')),  # all your app's API URLs here
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    # Removed invalid direct MetricViewSet path
    path('metrics/', MetricViewSet.as_view({'get': 'list'}), name='metrics'),
    path('prometheus-metrics/', exports.ExportToDjangoView),
    path('update-cpu/', update_metric_api, name='update_cpu'),
    path('met/', metrics_view, name='metrics_view'), 
     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
     path('addmet/', metrics_view, name='metrics_view'), 
]
