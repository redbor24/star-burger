# Generated by Django 3.2 on 2022-09-19 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0045_order_payment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restorans', to='foodcartapp.restaurant', verbose_name='Ресторан'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('u', 'Необработанный'), ('p', 'Обработанный'), ('i', 'Готовится')], db_index=True, default='u', max_length=1, verbose_name='Статус'),
        ),
    ]
