# Generated by Django 3.1.7 on 2021-04-15 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20210415_1823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='on_road',
            new_name='released',
        ),
    ]
