# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if (email and User.objects.filter(email=email).exclude(
                username=username).count()):
            raise forms.ValidationError(('This email address already exists.'))
        return email
