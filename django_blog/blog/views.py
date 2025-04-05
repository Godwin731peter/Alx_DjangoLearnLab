from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileUpdateForm

# Create your views here.
# registerong a user
def register_view(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('profile')
  
  else:
    form = CustomUserCreationForm()
  return render('blog/register.html', {'form': form})

def login_view(requuest):
  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('profile')
  else:
    form = AuthenticationForm()
  return render('blog/login.html', {'form': form})

def logout_view(request):
  logout(request)
  return redirect('login')

@login_required
def profile_view(request):
  if method.request == 'POST':
    form = ProfileUpdateForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      return redirect('profile')
  else:
    form = ProfileUpdateForm(instance=request.user)
  return render(request, 'blog/profile.html', {'user': request.user})