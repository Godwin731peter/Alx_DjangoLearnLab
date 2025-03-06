from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth.decorators import permission_required, user_passes_test
from .models import Book
from .models import Library
from .forms import BookForm


# Create your views here.
def list_books(request):
  books = Book.objects.all()
  return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
  model = Library
  template_name = "relationship_app/library_detail.html"
  context_object_name = "library"


def login_view(request):
  if request.method == "POST":
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('/')
  else:
    form = AuthenticationForm()
  return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(request, "logout.html")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# role checking fuctions
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
   if request.method == "POST":
      form = BookForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('book_list')
   else:
      form = BookForm()
   return render(request, 'relationship_app/book_for.html')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
   book = get_object_or_404(Book, id=book_id)
   if request.method == "POST":
      form = BookForm(request.POST, instance=book)
      if form.is_valid():
         form.save()
         return redirect('book_list')
      
   else:
      form = BookForm(instance=book)
   return render(request, 'relationship_app/book_form.html', {'form': for})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
   book = get_object_or_404(Book, id=book_id)
   if request.method == "POST":
      book.delete()
      return redirect('book_list')
   return render(request, 'relationship_app/book_confirm_delete', {'book': book})