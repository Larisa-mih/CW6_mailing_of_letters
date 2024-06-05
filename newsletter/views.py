from audioop import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from newsletter.forms import MailForm, ClientForm, MessageForm, MailManagerForm
from newsletter.models import Mail, Client, Message, LogAttempt
from newsletter.services import get_random_articles_cache


class HomePageView(TemplateView):
    template_name = 'newsletter/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        mailing = Mail.objects.all()
        clients = Client.objects.all()
        context['count_mail'] = mailing.count()
        context['mail_is_active'] = mailing.filter(mail_active=True).count()
        context['count_client'] = clients.count()
        context['count_client_unique'] = clients.values('email').distinct().count()
        context['random_article_list'] = get_random_articles_cache(3)
        return context


class MailListView(LoginRequiredMixin, ListView):
    """ Просмотр списка рассылок """
    model = Mail

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moderator').exists():
            queryset = queryset.filter(owner=user)
        return queryset


class MailDetailView(LoginRequiredMixin, DetailView):
    """ Просмотр деталей рассылки """
    model = Mail

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moderator').exists() and user != self.object.owner:
            raise PermissionDenied
        return self.object


class MailCreateView(LoginRequiredMixin, CreateView):
    """ Создание рассылки """
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('newsletter:mail_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['client'].queryset = Client.objects.filter(owner=user)
        form.fields['message'].queryset = Message.objects.filter(owner=user)
        return form

    def form_valid(self, form):
        mail = form.save()
        user = self.request.user
        mail.owner = user
        mail.save()
        return super().form_valid(form)


class MailUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование данных рассылки """
    model = Mail
    success_url = reverse_lazy('newsletter:mail_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            form.fields['client'].queryset = Client.objects.filter(owner=user)
            form.fields['message'].queryset = Message.objects.filter(owner=user)
        return form

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailForm
        elif user.groups.filter(name='moderator').exists():
            return MailManagerForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if (not user.is_superuser and user != self.object.owner and
                not user.groups.filter(name='moderator').exists()):
            raise PermissionDenied
        return self.object


class MailDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление рассылки """
    model = Mail
    success_url = reverse_lazy('newsletter:mail_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        return self.object


class ClientListView(LoginRequiredMixin, ListView):
    """ Просмотр списка клиентов """
    model = Client

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(owner=user)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Просмотр одного клиента"""
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        return self.object


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создание клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование данных клиента"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('newsletter:client_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление клиента"""
    model = Client
    success_url = reverse_lazy('newsletter:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        return self.object


class MessageListView(LoginRequiredMixin, ListView):
    """ Просмотр списка сообщений """
    model = Message

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(owner=user)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей сообщения"""
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        return self.object


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения"""
    model = Message
    success_url = reverse_lazy('newsletter:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        return self.object


class LogAttemptListView(LoginRequiredMixin, ListView):
    """Контроллер просмотра логов рассылки"""
    model = LogAttempt

    def get_queryset(self, *args, **kwargs):
        mail_pk = self.kwargs.get('mail_pk')
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(mail__pk=mail_pk)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['mail_pk'] = self.kwargs.get('mail_pk')
        return context

    def dispatch(self, request, *args, **kwargs):
        mail_pk = self.kwargs.get('mail_pk')
        user = self.request.user
        if not user.is_superuser and not Mail.objects.filter(pk=mail_pk, owner=user).exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
