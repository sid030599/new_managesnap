# Generated by Django 3.2.3 on 2022-12-26 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0007_auto_20221226_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycourses',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolledcourses', to=settings.AUTH_USER_MODEL),
        ),
    ]
