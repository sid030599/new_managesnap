from django import forms
from django.forms import ModelForm, Select
from django.contrib.auth.models import User
from .models import *
from courses.models import Groups

class student_verificationform(ModelForm):
    class Meta:
        model = temp_verification
        fields = ('college','roll_number','department','Year','section','semester')

class Profile_form(ModelForm):
    class Meta:
        model = Profile
        fields = ('college','roll_number','department','Year','section','semester')

class GroupsStudentForm(ModelForm):
    class Meta:
        model = Groups
        fields = ('students',)

        def __init__ (self):
            self.fields["students"].queryset = Groups.objects.filter(students=Profile.objects.filter(status = 's'))