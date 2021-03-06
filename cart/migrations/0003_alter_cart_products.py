# Generated by Django 3.2.4 on 2021-06-17 05:25
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_product_description"),
        ("cart", "0002_alter_cart_products"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="products",
            field=models.ManyToManyField(blank=True, default=None, to="products.Product"),
        ),
    ]
