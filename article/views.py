from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from article.forms import ArticleManagerForm
from article.models import Article
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from newsletter.services import get_article_list_from_cache


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'article.add_article'
    model = Article
    form_class = ArticleManagerForm
    success_url = reverse_lazy('article:articles')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'article.change_article'
    model = Article
    form_class = ArticleManagerForm

    def get_success_url(self):
        return reverse('article:article_detail', args=[self.kwargs.get('pk')])


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'article.delete_article'
    model = Article
    success_url = reverse_lazy('article:articles')


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        return get_article_list_from_cache()


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object
