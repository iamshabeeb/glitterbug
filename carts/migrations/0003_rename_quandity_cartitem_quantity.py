# Generated by Django 4.0.5 on 2022-06-24 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_rename_cartitems_cartitem_rename_car_cartitem_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='quandity',
            new_name='quantity',
        ),
    ]
