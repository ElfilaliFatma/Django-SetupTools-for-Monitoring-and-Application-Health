# Generated by Django 5.2.1 on 2025-05-16 21:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('current_value', models.FloatField()),
                ('unit', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AlertRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warning_threshold', models.FloatField()),
                ('critical_threshold', models.FloatField()),
                ('notify_email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alert_rules', to='monitoring_app.metric')),
            ],
        ),
    ]
