from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMMixin
from django.views.generic import ListViews
from django.shortcuts import render, get_object_or_404
from .models import Article

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

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from .models import Article

class ArticleListView(PermissionRequiredMixin, ListView):
    model = Article
    template_name = "articles/list.html"
    permission_required = "bookshelf.can_view"