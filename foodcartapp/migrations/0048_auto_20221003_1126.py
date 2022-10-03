# Generated by Django 3.2 on 2022-10-03 08:26

from django.db import migrations, models
import foodcartapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(max_length=255, verbose_name='Адрес заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_num',
            field=models.CharField(default=foodcartapp.models.order_mum_default, max_length=20, verbose_name='Номер заказа'),
        ),
    ]
