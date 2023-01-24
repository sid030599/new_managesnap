# Generated by Django 3.2.3 on 2023-01-13 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_temp_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp_verification',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='auth.user'),
            preserve_default=False,
        ),
    ]
