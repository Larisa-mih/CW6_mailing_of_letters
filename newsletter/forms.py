from newsletter.models import Mail, Client, Message
from users.forms import StyleFormMixin
from django import forms


class MailForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        exclude = ('mail_status', 'mail_active', 'owner')


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class MailManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        fields = ('mail_active',)
