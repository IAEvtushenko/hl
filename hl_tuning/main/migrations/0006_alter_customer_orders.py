# Generated by Django 3.2.5 on 2021-08-17 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210813_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(blank=True, related_name='related_customer', to='main.Order', verbose_name='Заказы покупателя'),
        ),
    ]