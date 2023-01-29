# Generated by Django 3.2.3 on 2023-01-26 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0024_auto_20230126_2341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manager_eveng',
            old_name='Event',
            new_name='event',
        ),
        migrations.AlterField(
            model_name='manager_eveng',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 26, 23, 52, 23, 492861)),
        ),
        migrations.AlterField(
            model_name='manager_notification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 26, 23, 52, 23, 492405)),
        ),
        migrations.AlterField(
            model_name='news_feed',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 26, 23, 52, 23, 491803)),
        ),
    ]