# Generated by Django 4.2.14 on 2024-07-28 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0004_remove_orderitem_discount"),
    ]

    operations = [
        migrations.AddField(
            model_name="useddiscount",
            name="order",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="order.orderitem",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("P", "PENDING"),
                    ("A", "ACCEPTED"),
                    ("S", "SHIPPED"),
                    ("C", "CANCELED"),
                ],
                default="P",
                max_length=1,
            ),
        ),
    ]