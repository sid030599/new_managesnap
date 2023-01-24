from datetime import datetime, timezone
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import *
# Create your models here.

class course(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    image = models.ImageField(upload_to='courseImg', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses', null=True)
    course_price = models.CharField(default='FREE', max_length=100)
    course_level = models.CharField(max_length=20, choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced')
        ],
        default='Beginner'
    )
    def __str__(self):
        return self.title 

class Unit(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    brief = models.TextField()
    due = models.DateField(null=True)
    released  = models.BooleanField(default = False)
    slug = models.SlugField(null=True, max_length=300, unique=False)

    def __str__(self):
        return self.title 
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title+self.course.title)
        super(Unit, self).save(*args, **kwargs)

class MyUnit(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(course,on_delete=models.CASCADE,default=1)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE,related_name='units',blank=True,default='unit1')

    def __str__(self):
        return self.user.username


class Lesson(models.Model):
    order = models.IntegerField(null=False, default=1)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,related_name='lessons')
    title = models.CharField(max_length=200)
    resource = models.FileField(upload_to='resources/', null=True, blank=True)
    #Files = models.ManyToManyField(LessonFile, blank=True)
    resource_name = models.CharField(max_length=100, null=False, default='Resource')
    resource_link = models.URLField(max_length=300, null=True, blank=True)
    isdone = models.BooleanField(default=False)
    released = models.BooleanField(default = False)
    def __str__(self):
        return self.title

class LessonFile(models.Model):
    lesson = models.ForeignKey(Lesson , on_delete = models.CASCADE,related_name='files')
    file = models.FileField(upload_to='resources/', null=True, blank=True)
    isdone  = models.BooleanField(default=False)
    def __str__(self):
        return self.lesson.title 

class MyLesson(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='lessons',blank=True,default='lesson1')
    isdone = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



# class profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     status = models.CharField(choices=status_choices, max_length=5, default='s')
#     college = models.CharField(max_length=100, choices=college_choice)

#     def __str__(self) -> str:
#         return self.user.username + '-' + self.status
class UserLessonCompletion(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    unlocked = models.BooleanField(default=False)
    timer_min_left = models.IntegerField(default=0)
    timer_sec_left = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.user.username} with {self.lesson.title}"






def create_course_units(sender, instance, created, **kwargs):
    if created:
        course = instance
        units = ['Announcement', 'Time Table', 'Syllabus', 'Assignment', 'Quiz', 'Caes', 'semester']
        for unit in units:
            course_unit = courseUnit.objects.create(course=course, name=unit)
            if unit in ['Assignment', 'Quiz', 'Caes', 'semester']:
                course_unit.is_assignment = True
                course_unit.save()

import os

class Files(models.Model):
    document = models.FileField(upload_to='documents', null=True, blank=True)

    def filename(self):
        return os.path.basename(self.document.name)


class courseTopic(models.Model):
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE,blank=True,null=True)
    course = models.ForeignKey(course, on_delete=models.CASCADE, related_name='courseTopics',blank=True,null=True)
    title = models.CharField(max_length=500)
    documents = models.ManyToManyField(Files, blank=True)
    info   = models.CharField(max_length=500, null=True, blank=True)
    link  = models.URLField(max_length=200, null=True, blank=True)
    released = models.BooleanField(default=False)
    created_by = models.CharField(max_length=20, choices=[
            ('M', 'Manager'),
            ('T', 'Teacher')
        ],
        default='T'
    )
    def __str__(self):
        return self.title

class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.RESTRICT)
    course = models.ForeignKey(course, on_delete=models.RESTRICT)
    razorpay_order_id = models.CharField(max_length=100,null=True)
    razorpay_payment_id = models.CharField(max_length=100,null=True)
    razorpay_signature =  models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.razorpay_order_id

def create_my_files(sender, instance,action="post_add", reverse=False ,*args, **kwargs):
    topic = instance
    my_topics = mytopics.objects.filter(coursetopic=topic)
    for my_topic in my_topics:
        my_topic.documents.clear()
        for document in topic.documents.all():
            file = myFiles.objects.create(document=document)
            my_topic.documents.add(file)
        my_topic.save()

# import pytz
# utc = pytz.UTC

class Assignment(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=500)
    documents = models.ManyToManyField(Files, blank=True)
    max_grades = models.PositiveIntegerField()
    deadline = models.DateTimeField()
    info   = models.CharField(max_length=500, null=True, blank=True)
    link  = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    released = models.BooleanField(default=False)
    def __str__(self):
        return self.title

    def submittable(self):
        current = self.deadline
        if(datetime.datetime.now(current.tzinfo) >= current):
            return False
        return True

# def create_my_assignment(sender, instance, *args, **kwargs):
#     assignment = instance
#     myCourses = mycourses.objects.filter(courses__id=assignment.course.id)
#     for course in myCourses:
#         my_assignment = myAssignment(user=course.user, assignment=assignment)
#         my_assignment.save()
#         grades.objects.create(myassignment = my_assignment)
    



class courseUnit(models.Model):
    name = models.CharField(max_length=8)
    course = models.ForeignKey(course, on_delete=models.CASCADE, null=True, related_name='units')
    topics = models.ManyToManyField(courseTopic, blank=True)
    assignments = models.ManyToManyField(Assignment, blank=True)
    is_assignment = models.BooleanField(default=False)

    def __str__(self):
        return self.name + "-" + self.course.title
    
def create_my_courseUnit(sender, instance,action="post_add", reverse=False ,*args, **kwargs):
    unit = instance
    topics = unit.topics.all()

    if myCourseUnit.objects.filter(courseunit=unit).count() ==0:
        myCourses = mycourses.objects.filter(courses__id=unit.course.id)
        for myCourse in myCourses:
            myCourseUnit.objects.create(user=myCourse.user, courseunit=unit)

    myunits = myCourseUnit.objects.filter(courseunit=unit)
    
    for myunit in myunits:
        myunit.coursetopics.clear()
        for topic in topics:
            # if not myunit.filter(coursetopics__id=topic):
            mytopic = mytopics(user=myunit.user, coursetopic=topic)
            mytopic.save()
            for doc in topic.documents.all():
                file = myFiles.objects.create(document=doc)
                mytopic.documents.add(file)
            myunit.coursetopics.add(mytopic)
            myunit.save()

def create_my_courseUnit_assignment(sender, instance,action="post_add", reverse=False ,*args, **kwargs):
    unit = instance
    assignments = unit.assignments.all()

    if myCourseUnit.objects.filter(courseunit=unit).count() ==0:
        myCourses = mycourses.objects.filter(courses__id=unit.course.id)
        for myCourse in myCourses:
            myCourseUnit.objects.create(user=myCourse.user, courseunit=unit)

    myunits = myCourseUnit.objects.filter(courseunit=unit)
    
    for myunit in myunits:
        myunit.course_assignments.clear()
        for assignment in assignments:
            # if not myunit.filter(coursetopics__id=topic):
            my_assignment = myAssignment(user=myunit.user, assignment=assignment)
            my_assignment.save()
            grades.objects.create(myassignment = my_assignment)
            myunit.course_assignments.add(my_assignment)
            myunit.save()

group_statuses = [
    ('d', 'Default'),
    ('c', 'Custom')
]

class Groups(models.Model):
    
    name    = models.CharField(max_length=50)
    students = models.ManyToManyField(Profile, related_name="enrolled_groups")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    status    = models.CharField(choices=group_statuses, max_length=5, default='d')
    enrolled_courses = models.ManyToManyField(course)

    def __str__(self):
        return self.created_by.username + "-" + self.status + str(self.id)
    



class mycourses(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolledcourses')
    courses = models.ForeignKey(course, on_delete=models.RESTRICT,related_name='courses',default=course.objects.all().first().id)
    courses = models.ManyToManyField(course, related_name="mycourses", blank=True)
    paid = models.BooleanField(default = False)
    def __str__(self):
        return self.user.username

class myFiles(models.Model):
    document = models.ForeignKey(Files, on_delete=models.CASCADE)
    done     = models.BooleanField(default=False)
    

class mytopics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coursetopic  = models.ForeignKey(courseTopic, on_delete=models.CASCADE)
    documents = models.ManyToManyField(myFiles, blank=True)
    done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username + "-" + self.coursetopic.title


class myAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='my_assignments')
    upload = models.FileField(upload_to='documents', validators=[FileExtensionValidator(allowed_extensions=["pdf"])], null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.assignment.title

class grades(models.Model):
    myassignment = models.OneToOneField(myAssignment, on_delete=models.CASCADE, related_name='grades')
    grades = models.PositiveIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    is_graded = models.BooleanField(default=False)
    graded_at = models.DateTimeField(auto_now=True)



class myCourseUnit(models.Model):
    courseunit = models.ForeignKey(courseUnit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coursetopics = models.ManyToManyField(mytopics, blank=True)
    course_assignments = models.ManyToManyField(myAssignment, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + "-" + self.courseunit.name

class News_feed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    news = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField(default = datetime.datetime.now())

    def __str__(self):
        return self.user.username

class Manager_notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    notification = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField(default = datetime.datetime.now())

    def __str__(self):
        return self.user.username



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        mycourses.objects.create(user=instance)
        Profile.objects.create(user=instance)



# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)

# post_save.connect(create_my_topic, sender=courseTopic)
# post_save.connect(create_my_assignment, sender=Assignment)
post_save.connect(create_course_units, sender=course)

m2m_changed.connect(create_my_courseUnit, sender=courseUnit.topics.through)
m2m_changed.connect(create_my_courseUnit_assignment, sender=courseUnit.assignments.through)
m2m_changed.connect(create_my_files, sender=courseTopic.documents.through)