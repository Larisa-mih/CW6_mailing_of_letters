from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
app_name = UsersConfig.name

from django.urls import path
from users.views import UserCreateView, email_verification, UserPasswordResetView, ProfileView, UsersListView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='token'),
    path('reset-password/', UserPasswordResetView.as_view(), name='reset_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('list/', UsersListView.as_view(), name='users'),

]
