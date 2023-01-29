# Generated by Django 3.2.3 on 2023-01-26 18:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0023_auto_20230123_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager_notification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 26, 23, 41, 15, 52929)),
        ),
        migrations.AlterField(
            model_name='news_feed',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 26, 23, 41, 15, 52443)),
        ),
        migrations.CreateModel(
            name='Manager_Eveng',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Event', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 1, 26, 23, 41, 15, 53399))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]