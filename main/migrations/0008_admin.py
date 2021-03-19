# Generated by Django 3.1.7 on 2021-03-19 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210319_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.CharField(blank=True, max_length=120, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='admin', serialize=False, to='main.user')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'admin_info',
            },
        ),
    ]
