# Generated by Django 3.2.3 on 2023-05-03 19:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0008_auto_20230122_2358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('max_grades', models.PositiveIntegerField()),
                ('deadline', models.DateTimeField()),
                ('info', models.CharField(blank=True, max_length=500, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('released', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='courseImg')),
                ('course_price', models.CharField(default='FREE', max_length=100)),
                ('course_level', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner', max_length=20)),
                ('released', models.BooleanField(default=False)),
                ('is_paused', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='courseTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('info', models.CharField(blank=True, max_length=500, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('released', models.BooleanField(default=False)),
                ('created_by', models.CharField(choices=[('M', 'Manager'), ('T', 'Teacher')], default='T', max_length=20)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courseTopics', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='courseUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8)),
                ('is_assignment', models.BooleanField(default=False)),
                ('assignments', models.ManyToManyField(blank=True, to='courses.Assignment')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='units', to='courses.course')),
                ('topics', models.ManyToManyField(blank=True, to='courses.courseTopic')),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(blank=True, null=True, upload_to='documents')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=200)),
                ('resource', models.FileField(blank=True, null=True, upload_to='resources/')),
                ('resource_name', models.CharField(default='Resource', max_length=100)),
                ('resource_link', models.URLField(blank=True, max_length=300, null=True)),
                ('isdone', models.BooleanField(default=False)),
                ('released', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='myAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(blank=True, null=True, upload_to='documents', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('uploaded_at', models.DateTimeField(auto_now=True)),
                ('done', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_assignments', to='courses.assignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='myFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField(default=False)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.files')),
            ],
        ),
        migrations.CreateModel(
            name='UserLessonCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('unlocked', models.BooleanField(default=False)),
                ('timer_min_left', models.IntegerField(default=0)),
                ('timer_sec_left', models.IntegerField(default=0)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('brief', models.TextField()),
                ('due', models.DateField(null=True)),
                ('released', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=300, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_order_id', models.CharField(max_length=100, null=True)),
                ('razorpay_payment_id', models.CharField(max_length=100, null=True)),
                ('razorpay_signature', models.CharField(max_length=100, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='News_feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('unit', models.ForeignKey(blank=True, default='unit1', on_delete=django.db.models.deletion.CASCADE, related_name='units', to='courses.unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='mytopics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField(default=False)),
                ('coursetopic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.coursetopic')),
                ('documents', models.ManyToManyField(blank=True, to='courses.myFiles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isdone', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(blank=True, default='lesson1', on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.lesson')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='myCourseUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField(default=False)),
                ('course_assignments', models.ManyToManyField(blank=True, to='courses.myAssignment')),
                ('coursetopics', models.ManyToManyField(blank=True, to='courses.mytopics')),
                ('courseunit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courseunit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='mycourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('courses', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='mycourses', to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolledcourses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manager_notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manager_Eveng',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LessonFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='resources/')),
                ('isdone', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='courses.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.unit'),
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('d', 'Default'), ('c', 'Custom')], default='d', max_length=5)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_groups', to=settings.AUTH_USER_MODEL)),
                ('enrolled_courses', models.ManyToManyField(to='courses.course')),
                ('students', models.ManyToManyField(related_name='enrolled_groups', to='account.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='grades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grades', models.PositiveIntegerField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=100, null=True)),
                ('is_graded', models.BooleanField(default=False)),
                ('graded_at', models.DateTimeField(auto_now=True)),
                ('myassignment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='courses.myassignment')),
            ],
        ),
        migrations.AddField(
            model_name='coursetopic',
            name='documents',
            field=models.ManyToManyField(blank=True, to='courses.Files'),
        ),
        migrations.AddField(
            model_name='coursetopic',
            name='posted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.profile'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='courses.course'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='documents',
            field=models.ManyToManyField(blank=True, to='courses.Files'),
        ),
    ]
