# Generated by Django 3.1.7 on 2021-04-15 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210415_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalroute',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.student'),
        ),
    ]
