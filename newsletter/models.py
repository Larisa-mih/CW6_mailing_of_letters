from django.utils import timezone
from django.utils.translation import gettext as _
from django.db import models
from config import settings


NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """ Клиент """
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=20, verbose_name='Отчество', **NULLABLE)
    email = models.EmailField(verbose_name='Электронный адрес')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.first_name}{self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """ Сообщение """
    message_title = models.CharField(max_length=100, verbose_name='Тема письма')
    message_content = models.TextField(verbose_name='Содержание')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.message_title}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'


class Mail(models.Model):
    """ Рассылка """

    class PeriodicityOfMail(models.TextChoices):
        ONCE_DAY = "Раз в день", _("Раз в день")
        ONCE_WEEK = "Раз в неделю", _("Раз в неделю")
        ONCE_MONTH = "Раз в месяц", _("Раз в месяц")

    class StatusOfMail(models.TextChoices):
        CREATED = "Создана", _("Создана")
        LAUNCHED = "Запущена", _("Запущена")
        FINISHED = "Завершена", _("Завершена")

    title = models.CharField(max_length=100, verbose_name='Тема рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    client = models.ManyToManyField(Client, verbose_name='Клиент', related_name='client')
    mail_datetime = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    mail_datetime_last = models.DateTimeField(default=timezone.now, verbose_name='Следующая отправка', **NULLABLE)
    mail_periodicity = models.CharField(verbose_name='Периодичность', choices=PeriodicityOfMail, default=PeriodicityOfMail.ONCE_DAY)
    mail_status = models.CharField(verbose_name='Статус отправки', choices=StatusOfMail, default=StatusOfMail.CREATED)
    mail_active = models.BooleanField(verbose_name='Активность рассылки', default=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.mail_status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('set_deactivate', 'Can deactivate mail'),
            ('view_all_mail', 'Can view all mail'),
        ]


class LogAttempt(models.Model):
    """Попытка рассылки"""
    class StatusOfLogAttempt(models.TextChoices):
        SUCCESS = "Успешно", _("Успешно")
        FAILED = "Безуспешно", _("Безуспешно")

    attempt_datetime = models.DateTimeField(verbose_name='Дата и время последней попытки', auto_now_add=True)
    attempt_status = models.CharField(max_length=50, choices=StatusOfLogAttempt, verbose_name="Cтатус попытки")
    server_response = models.CharField(verbose_name="Ответ почтового сервера", **NULLABLE)
    mail = models.ForeignKey(Mail, verbose_name="Рассылка", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mail}, {self.attempt_datetime}, {self.attempt_status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
