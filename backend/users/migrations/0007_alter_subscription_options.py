# Generated by Django 4.1 on 2023-03-29 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_user_is_staff"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscription",
            options={
                "ordering": ("user",),
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
            },
        ),
    ]