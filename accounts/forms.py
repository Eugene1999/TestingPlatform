from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django import forms

from .models import User


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        
        if password and password2 and password != password2:
            raise ValidationError(_('Invalid passwords - passwords didn`t match'))

        return password2

    def save(self, commit=True):
        user = User(username=self.cleaned_data["username"])
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
