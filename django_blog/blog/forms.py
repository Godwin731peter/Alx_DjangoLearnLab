from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class CustomUserCreationForm(UserCreationForm):
  email = forms.EmailField(required=True)

  class Meta:
    Model = User
    Fields = ['Username', 'email', 'password']

class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['email']

# blog/forms.py

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
