# Generated by Django 3.2.3 on 2023-01-12 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(blank=True, max_length=500, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=200, null=True)),
                ('status', models.CharField(choices=[('p', 'Principal'), ('t', 'Teacher'), ('s', 'Student'), ('m', 'Management')], default='s', max_length=5)),
                ('profile_status', models.BooleanField(default=False)),
                ('semester', models.CharField(max_length=10)),
                ('section', models.CharField(max_length=10)),
                ('Year', models.DateField()),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.college')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]