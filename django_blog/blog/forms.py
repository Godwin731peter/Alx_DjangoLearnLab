from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
  email = forms.EmailField(required=True)

  class Meta:
    Model = User
    Fields = ['Username', 'email', 'password']

class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['email']