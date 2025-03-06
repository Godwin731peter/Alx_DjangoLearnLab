from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from relationship_app import views
from .views import list_books, LibraryDetailView
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view

urlpatterns = [
  path("books/", list_books, name="list_books"),
  path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
  path("", include("relationship_app.urls")),
  path('register/', views.register_view, name='register'),
  path('login/', LoginView.as_view(template_name='login.html'), name='login'),
  path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
  path('admin-view/', admin_view, name='admin_view'),
  path('librarian-view/', librarian_view, name='librarian_view'),
  path('member-view/', member_view, name='member_view'),
  path('books/add/', views.add_book, name='add_book'),
  path('books/edit/add_book/', views.edit_book, name='edit_book'),
  path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]