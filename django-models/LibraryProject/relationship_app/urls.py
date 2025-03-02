from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view
from .views import list_books, LibraryDetailView

urlpatterns = [
  path("books/", list_books, name="list_books"),
  path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
  path("", include("relationship_app.urls")),
  path('register/', register_view, name='register'),
  path('login/', LoginView.as_view(template_name='login.html'), name='login'),
  path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]