# Generated by Django 2.2.1 on 2019-05-03 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20190503_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, to='catalog.CartItem'),
        ),
    ]
