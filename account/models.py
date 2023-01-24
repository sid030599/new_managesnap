from django.db import models


from datetime import datetime, timezone
from django.core.validators import FileExtensionValidator

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
    ('s', 'Student'),
    ('m','Management')
]

class College(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


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
    department = models.CharField(max_length=500, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    full_name               =       models.CharField(max_length=100, blank=True, null=True)
    email                   =       models.EmailField()
    college = models.ForeignKey(College,on_delete = models.CASCADE,null=True, blank=True)
    
    slug = models.SlugField(max_length=200, editable=False, null=True, blank=True)
    status = models.CharField(choices=status_choices, max_length=5, default='s')
    is_verified = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    semester                =       models.CharField(max_length=10)
    section                =       models.CharField(max_length=10)
    Year                =       models.DateField(default=datetime.datetime.now)
    roll_number         = models.IntegerField(blank=True,null=True)
    #college status : undefined 

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class temp_verification(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    college = models.ForeignKey(College,on_delete=models.DO_NOTHING)
    semester                =       models.CharField(max_length=10)
    section                =       models.CharField(max_length=10)
    Year                =       models.DateField(default=datetime.datetime.now)
    roll_number         = models.IntegerField(blank=True,null=True)
    department = models.CharField(max_length=500, null=True, blank=True)
    is_varified         = models.BooleanField(default=False)
    is_rejected         = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
