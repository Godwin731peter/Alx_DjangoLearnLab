from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CustomUserCreationForm, ProfileUpdateForm, CommentForm

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
  return render(request, 'blog/profile.html', {'form': form, 'user': request.user})

class PostListView(ListView):
  model = Post
  template_name = 'blog/post_list.html'
  context_object_name = 'posts'
  ordering = ['-published_date']

class PostDetailView(DetailView):
  model = Post
  template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['title', 'content']
  template_name = 'blog/post_form.html'

  def form_valid(self, form):
    for.instance.author = self.request.user
    return super().form_valid(form)
  
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['title', 'content']
  template_name = 'blog/post_form.html'

  def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

  def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author 
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('post_detail', pk=post.id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('post_detail', pk=comment.post.id)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    if comment.author == request.user:
        comment.delete()
    return redirect('post_detail', pk=post_id)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_id)
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
