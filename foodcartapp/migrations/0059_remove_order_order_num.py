# Generated by Django 3.2 on 2022-10-05 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0058_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_num',
        ),
    ]
