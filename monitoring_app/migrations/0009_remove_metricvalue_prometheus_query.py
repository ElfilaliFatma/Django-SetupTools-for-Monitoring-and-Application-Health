# Generated by Django 5.2.1 on 2025-05-31 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring_app', '0008_metricvalue_prometheus_query'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metricvalue',
            name='prometheus_query',
        ),
    ]
