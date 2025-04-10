from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from django import forms

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
   tags = forms.CharField(required=False, help_text="Comma-separated list of tags")
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        tag_names = self.cleaned_data['tags'].split(',')
        instance.tags.clear()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name.strip())
            instance.tags.add(tag)
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
        }
