import os
import django

# set up django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django-models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query to get all books by a specific author
def get_books_by_author(author_name):
  author = Author.objects.get(name=author_name)
  books = Book.objects.filter(author=author)
  return books

# Query to list all books in a library
def get_books_library(library_name):
  library = Library.objects.get(name=library_name)
  return library.books.all()

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
  library = Library.objects.get(name=library_name)
  return Librarian.objects.get(library=library)