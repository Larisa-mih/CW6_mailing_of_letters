import secrets
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from users.forms import UserRegisterForm, UserPasswordResetForm, UserProfileForm
from users.models import User
from config.settings import DEFAULT_FROM_EMAIL
from users.service import generate_password


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Здравствуйте, для подтверждения регистрации перейдите по ссылке {url}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserPasswordResetView(PasswordResetView):
    model = User
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if self.request.method == 'POST':
            user_email = self.request.POST.get('email')
            user = User.objects.filter(email=user_email).first()
            if user:
                new_password = generate_password(16)
                user.set_password(new_password)
                user.save()
                try:
                    send_mail(
                            subject="Восстановление пароля на сайте 'Рассылка'",
                            message=f"Здравствуйте!"
                            f"Ваш пароль для доступа на сайт 'Рассылка' изменен:\n"
                            f"Данные для входа:\n"
                            f"Email: {user_email}\n"
                            f"Пароль: {new_password}",
                            from_email=DEFAULT_FROM_EMAIL,
                            recipient_list=[user.email]
                            )
                except Exception:
                    print(f'Ошибка при отправке на почту {user_email}')
                return HttpResponseRedirect(reverse('users:login'))

        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_edit_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UsersListView(PermissionRequiredMixin, ListView):
    """ Просмотр списка рассылок """
    model = User
    permission_required = "view_all_users"
