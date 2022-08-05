# Generated by Django 4.1 on 2022-08-05 19:33

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("fullname", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "admin"),
                            ("creator", "creator"),
                            ("sale", "sale"),
                        ],
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("last_login", models.DateTimeField(null=True)),
            ],
            options={
                "ordering": ("created_at",),
            },
            bases=(models.Model, django.contrib.auth.models.PermissionManager),
        ),
    ]
