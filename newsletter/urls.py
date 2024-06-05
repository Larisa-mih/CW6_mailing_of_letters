from django.urls import path
from newsletter.views import MailListView, MailDetailView, MailCreateView, MailUpdateView, MailDeleteView, \
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, MessageListView, \
    HomePageView, MessageCreateView, MessageDetailView, MessageDeleteView, MessageUpdateView, LogAttemptListView
from newsletter.apps import NewsletterConfig
app_name = NewsletterConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),

    path('mail/', MailListView.as_view(), name="mail_list"),
    path('mail/<int:pk>/', MailDetailView.as_view(), name="mail_detail"),
    path('mail/create/', MailCreateView.as_view(), name="mail_create"),
    path('mail/update/<int:pk>/', MailUpdateView.as_view(), name='mail_update'),
    path('mail/delete/<int:pk>/', MailDeleteView.as_view(), name='mail_delete'),

    path('client/', ClientListView.as_view(), name="client_list"),
    path('client/<int:pk>/', ClientDetailView.as_view(), name="client_detail"),
    path('client/create/', ClientCreateView.as_view(), name="client_create"),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('message/', MessageListView.as_view(), name="message_list"),
    path('message/<int:pk>/', MessageDetailView.as_view(), name="message_detail"),
    path('message/create/', MessageCreateView.as_view(), name="message_create"),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('mail/<int:mail_pk>/logs/', LogAttemptListView.as_view(), name='log_list'),

]
