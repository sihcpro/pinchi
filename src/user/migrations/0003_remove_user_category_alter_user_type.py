# Generated by Django 4.2.14 on 2024-07-28 22:11

from django.db import migrations, models
import user.enums


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_user_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="category",
        ),
        migrations.AlterField(
            model_name="user",
            name="type",
            field=models.CharField(
                choices=[("I", "INTERNAL_STAFF"), ("E", "EXTERNAL_CUSTOMER")],
                default=user.enums.UserType["EXTERNAL_CUSTOMER"].value,
                max_length=1,
            ),
        ),
    ]
