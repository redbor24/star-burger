# Generated by Django 3.2 on 2022-09-16 13:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_auto_20220916_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('u', 'Необработанный'), ('p', 'Обработанный')], db_index=True, default='u', max_length=1, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='orderlines',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(1, 'Цена должна быть больше 0')], verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='orderlines',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество, шт.'),
        ),
    ]