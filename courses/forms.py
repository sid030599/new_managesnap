from django import forms
from django.contrib.auth.models import User
from .models import Lesson,LessonFile,News_feed,Manager_notification,Manager_Eveng


class userform(forms.ModelForm):
    pass2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    def clean_pass2(self):
        pass2 = self.cleaned_data.get("pass2")

        return pass2
    def save(self, commit=True):
        user = super(userform, self).save(commit=False)
        user.set_password(self.cleaned_data['pass2'])
        if commit:
            user.save()
        return user

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ( 'title', 'resource',  'resource_link')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'title', 'class': 'w3-input w3-border w3-round'}),
            'duration_Seconds': forms.TimeInput(attrs={'placeholder': 'expected duration to complete the lesson', 'class': 'w3-input w3-border w3-round'}),
            'duration_Minutes': forms.TimeInput(attrs={'placeholder': 'expected duration to complete the lesson', 'class': 'w3-input w3-border w3-round'}),
            'xp': forms.NumberInput(attrs={'placeholder': 'rewarded xp on completion', 'class': 'w3-input w3-border w3-round'}),
            'resource': forms.FileInput(attrs={'placeholder': 'tell us brief about the course', 'class': 'w3-input w3-border w3-round','multiple':True}),
            'resource_name': forms.TextInput(attrs={'placeholder': 'name for the resource file ', 'class': 'w3-input w3-border w3-round'}),
            'resource_link': forms.URLInput(attrs={'placeholder': 'tell us brief about the course', 'class': 'w3-input w3-border w3-round'}),
        }

class LessonFileForm(forms.ModelForm):
    class Meta:
        model = LessonFile
        fields = ('file',)

class ManagerNotificationForm(forms.ModelForm):
    class Meta:
        model = Manager_notification
        fields = ('notification',)

class NewsFeedForm(forms.ModelForm):
    class Meta:
        model = News_feed
        fields = ('news',)

class ManagerEventForm(forms.ModelForm):
    class Meta:
        model = Manager_Eveng
        fields = ('event',)