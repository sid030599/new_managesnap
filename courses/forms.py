from django import forms
from django.contrib.auth.models import User



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

