# Generated by Django 3.1.7 on 2021-03-19 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210307_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='admin_id',
        ),
        migrations.AddField(
            model_name='driver',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='age',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='driver_id',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='driver', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='driver',
            table='driver_info',
        ),
    ]
