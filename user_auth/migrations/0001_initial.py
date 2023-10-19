# Generated by Django 4.2 on 2023-10-19 12:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserModel",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "username",
                    models.CharField(
                        max_length=20, unique=True, verbose_name="Имя организации"
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="Почта",
                    ),
                ),
                ("is_verify_email", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="пользователь_профили",
                        to="auth.group",
                        verbose_name="Группы",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="пользователь_профили",
                        to="auth.permission",
                        verbose_name="Права пользователя",
                    ),
                ),
            ],
            options={
                "verbose_name": "Профиль",
                "verbose_name_plural": "Список профилей",
                "ordering": ("username",),
            },
        ),
    ]
