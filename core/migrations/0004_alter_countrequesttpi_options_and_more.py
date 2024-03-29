# Generated by Django 4.2 on 2023-11-30 18:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_countrequesttpi"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="countrequesttpi",
            options={
                "ordering": ("created_at",),
                "verbose_name": "Запрос",
                "verbose_name_plural": "Список запросов",
            },
        ),
        migrations.RenameField(
            model_name="countrequesttpi",
            old_name="time",
            new_name="created_at",
        ),
        migrations.AddField(
            model_name="countrequesttpi",
            name="data_2gis",
            field=models.JSONField(blank=True, null=True, verbose_name="Данные 2GIS"),
        ),
        migrations.AddField(
            model_name="countrequesttpi",
            name="data_ai",
            field=models.JSONField(blank=True, null=True, verbose_name="Данные AI"),
        ),
        migrations.AddField(
            model_name="countrequesttpi",
            name="data_yandex",
            field=models.JSONField(
                blank=True,
                null=True,
                verbose_name="Данные ЯндексАПИ",
            ),
        ),
        migrations.AddField(
            model_name="countrequesttpi",
            name="status_2gis",
            field=models.BooleanField(default=True, verbose_name="Состояние 2GIS"),
        ),
        migrations.AddField(
            model_name="countrequesttpi",
            name="status_ai",
            field=models.BooleanField(default=True, verbose_name="Состояние AI"),
        ),
        migrations.AddField(
            model_name="countrequesttpi",
            name="status_yandex",
            field=models.BooleanField(default=True, verbose_name="Состояние ЯндексАПИ"),
        ),
    ]
