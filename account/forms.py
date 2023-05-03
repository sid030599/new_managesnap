from django import forms
from django.forms import ModelForm, Select
from django.contrib.auth.models import User
from .models import *
from courses.models import Groups
from itertools import chain


class student_verificationform(ModelForm):
    class Meta:
        model = temp_verification
        fields = ('college','roll_number','department','Year','section','semester')

class Profile_form(ModelForm):
    class Meta:
        model = Profile
        fields = ('college','roll_number','department','Year','section','semester')

class GroupsStudentForm(forms.Form):

    def __init__(self,id, *args, **kwargs):
        super(GroupsStudentForm, self).__init__(*args, **kwargs)
        
        default_groups_students = Groups.objects.get(id=id)
        
        All_student = list(chain(Profile.objects.filter(status="s"))) 
        
        self.fields['students'] = forms.ChoiceField(choices=[(x.id, x) for x  in list(set(All_student) ^ set(list(chain(default_groups_students.students.all())))) ])
        
        
    
       