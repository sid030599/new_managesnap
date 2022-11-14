from datetime import datetime, timezone
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
status_choices = [
    ('p', 'Principal'),
    ('t', 'Teacher'),
    ('s', 'Student')
]

class College(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

colleges = College.objects.all()

college_choice = []

for college in colleges:
    college_choice.append((college.name, college.name))


#User._meta.get_field('email')._unique = True

def current_year():
        return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year()+10)(value)

    
gender_choices = (('M', 'MALE'),
('F', 'FEMALE'),
('O', 'OTHER'))
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # personal details
    bio = models.CharField(max_length=500, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    full_name               =       models.CharField(max_length=100, blank=True, null=True)
    gender                  =       models.CharField(choices=gender_choices, max_length=2, blank=True, null=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state                   =       models.CharField(max_length=40, null=True, blank=True)
    city                    =       models.CharField(max_length=40, null=True, blank=True)
    linkedin                =       models.URLField(max_length=200, null=True, blank=True)
    github                  =       models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    ph_num = models.CharField(max_length=15, null=True, blank=True)
    skills = models.CharField(max_length=400, null=True, blank=True)
    languages = models.CharField(max_length=400, null=True, blank=True)
    default_coding_lang = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to='profile_resumes', null=True, blank=True)

    # educational info
    institute_name          =       models.CharField(max_length=100, null=True, blank=True)
    institute_location = models.CharField(max_length=100, null=True, blank=True)
    yearOfPassing           =       models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1980), max_value_current_year], null=True, blank=True)
    current_cgpa       =       models.FloatField(null=True, validators=[MaxValueValidator(100), MinValueValidator(0)], blank=True)
    out_of        =       models.FloatField(null=True, validators=[MaxValueValidator(100), MinValueValidator(0)], blank=True)
    # professional info
    workExp                 =       models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(50)], blank=True)
    current_CTC             =       models.FloatField(null=True, blank=True)
    notice_period = models.IntegerField(null=True, blank=True)
    willing_to_relocate = models.BooleanField(default=True, null=True, blank=True)
    expected_CTC            =       models.FloatField(null=True, blank=True)
    current_company         =       models.CharField(max_length=200, null=True, blank=True)
    dream_company           =       models.CharField(max_length=200, null=True, blank=True)
    designation             =       models.CharField(max_length=100, null=True, blank=True)
    xp = models.IntegerField(null=True, default=100, blank=True)
    techsnap_cash = models.IntegerField(null=True, default=999, blank=True)
    college = models.CharField(max_length=100, choices=college_choice,default = 'abc')
    slug = models.SlugField(max_length=200, editable=False, null=True, blank=True)
    status = models.CharField(choices=status_choices, max_length=5, default='s')
    # is_student = models.BooleanField(default=True)
    # is_creator = models.BooleanField(default=False)
    # is_hr = models.BooleanField(default=False)
    teammates = models.ManyToManyField(User, related_name='teammates', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(Profile, self).save()
        self.slug = slugify(self.user.username)
        super(Profile, self).save()

    def courseprofile(self):
        return self.course_profile.all()

    # @property
    # def num_ForumPosts(self):
    #     return ForumPost.objects.filter(user=self).count()







# class profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     status = models.CharField(choices=status_choices, max_length=5, default='s')
#     college = models.CharField(max_length=100, choices=college_choice)

#     def __str__(self) -> str:
#         return self.user.username + '-' + self.status

class course(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    image = models.ImageField(upload_to='courseImg', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses', null=True)

    def __str__(self):
        return self.title 



def create_course_units(sender, instance, created, **kwargs):
    if created:
        course = instance
        units = ['Announcement', 'Time Table', 'Syllabus', 'Assignment', 'Quiz', 'Caes', 'semester', 'Unit Lessons']
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
    course = models.ForeignKey(course, on_delete=models.CASCADE, related_name='courseTopics')
    title = models.CharField(max_length=500)
    documents = models.ManyToManyField(Files, blank=True)
    info   = models.CharField(max_length=500, null=True, blank=True)
    link  = models.URLField(max_length=200, null=True, blank=True)
    released = models.BooleanField(default=False)
    def __str__(self):
        return self.title

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
    students = models.ManyToManyField(User, related_name="enrolled_groups")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    status    = models.CharField(choices=group_statuses, max_length=5, default='d')
    enrolled_courses = models.ManyToManyField(course)

    def __str__(self):
        return self.created_by.username + "-" + self.status + str(self.id)
    



class mycourses(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='enrolledcourses')
    courses = models.ManyToManyField(course, related_name="mycourses", blank=True)

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

    def __str__(self):
        return self.user.username + "-" + self.courseunit.name


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