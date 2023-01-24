# Generated by Django 3.2.3 on 2023-01-15 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_profile_email'),
        ('courses', '0012_manager_notification_news_feed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='students',
            field=models.ManyToManyField(related_name='enrolled_groups', to='account.Profile'),
        ),
    ]
