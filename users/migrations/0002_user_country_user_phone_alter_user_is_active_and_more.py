# Generated by Django 5.0.6 on 2024-06-05 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="country",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="страна"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(
                blank=True, max_length=35, null=True, verbose_name="телефон"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="active",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=100, verbose_name="имя"),
        ),
    ]