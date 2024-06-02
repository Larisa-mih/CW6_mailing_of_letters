# Generated by Django 5.0.6 on 2024-05-28 01:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=20, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=20, verbose_name="Фамилия")),
                (
                    "surname",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="Отчество"
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="Электронный адрес"),
                ),
                (
                    "comment",
                    models.TextField(blank=True, null=True, verbose_name="Комментарий"),
                ),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "message_title",
                    models.CharField(max_length=100, verbose_name="Тема письма"),
                ),
                ("message_content", models.TextField(verbose_name="Содержание")),
            ],
            options={
                "verbose_name": "Сообщение для рассылки",
                "verbose_name_plural": "Сообщения для рассылки",
            },
        ),
        migrations.CreateModel(
            name="Mail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=100, verbose_name="Тема рассылки"),
                ),
                (
                    "mail_datetime",
                    models.DateTimeField(verbose_name="Начало отправки рассылки"),
                ),
                (
                    "mail_datetime_last",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Последняя дата отправки рассылки",
                    ),
                ),
                (
                    "mail_periodicity",
                    models.CharField(
                        choices=[
                            ("Раз в день", "Раз в день"),
                            ("Раз в неделю", "Раз в неделю"),
                            ("Раз в месяц", "Раз в месяц"),
                        ],
                        verbose_name="Периодичность",
                    ),
                ),
                (
                    "mail_status",
                    models.CharField(
                        choices=[
                            ("Создана", "Создана"),
                            ("Запущена", "Запущена"),
                            ("Завершена", "Завершена"),
                        ],
                        default="Создана",
                        verbose_name="Статус отправки",
                    ),
                ),
                (
                    "mail_active",
                    models.BooleanField(
                        default=True, verbose_name="Активность рассылки"
                    ),
                ),
                (
                    "client",
                    models.ManyToManyField(
                        related_name="client",
                        to="newsletter.client",
                        verbose_name="Клиент",
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="newsletter.message",
                        verbose_name="Сообщение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.CreateModel(
            name="LogAttempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attempt_datetime",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата и время последней попытки"
                    ),
                ),
                (
                    "attempt_status",
                    models.CharField(
                        choices=[("success", "Успешно"), ("fail", "Не успешно")],
                        max_length=50,
                        verbose_name="Cтатус попытки",
                    ),
                ),
                (
                    "server_response",
                    models.CharField(
                        blank=True, null=True, verbose_name="Ответ почтового сервера"
                    ),
                ),
                (
                    "mail_settings",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="newsletter.mail",
                        verbose_name="Настройка рассылки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылки",
            },
        ),
    ]
