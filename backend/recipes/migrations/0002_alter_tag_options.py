# Generated by Django 4.1 on 2023-03-23 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tag",
            options={
                "ordering": ("name",),
                "verbose_name": "Тэг",
                "verbose_name_plural": "Тэги",
            },
        ),
    ]
