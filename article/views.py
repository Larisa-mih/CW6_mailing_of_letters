from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from article.forms import ArticleManagerForm
from article.models import Article
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'article.add_article'
    model = Article
    form_class = ArticleManagerForm
    success_url = reverse_lazy('article:articles')


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


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object
