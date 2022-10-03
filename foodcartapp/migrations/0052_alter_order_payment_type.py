# Generated by Django 3.2 on 2022-10-03 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0051_alter_orderlines_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('cashless', 'По карте при оформлении'), ('cash', 'Наличными при доставке')], db_index=True, max_length=12, verbose_name='Тип оплаты'),
        ),
    ]
