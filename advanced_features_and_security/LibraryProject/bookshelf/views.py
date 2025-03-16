from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListViews
from django.shortcuts import render, get_object_or_404
from .models import Article, Book
from .forms import ExampleForm

# Create your views here.
@permission_required('bookshelf.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_article(request):
    # Logic for creating an article
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # Logic for editing an article
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    # Redirect or return response
    pass


class ArticleListView(PermissionRequiredMixin, ListView):
    model = Article
    template_name = "articles/list.html"
    permission_required = "bookshelf.can_view" 

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


def search_books(request):
    form = BookSearchForm(request.GET)
    books = Book.object.none()
    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        books = Book.objects.filter(title_icontains=query)
    return render(request, 'bookshelf/book_list.html', {'form': form, 'books': books})