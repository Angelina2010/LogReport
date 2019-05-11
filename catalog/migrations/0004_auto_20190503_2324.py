# Generated by Django 2.2.1 on 2019-05-03 23:24

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=catalog.models.image_folder),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('item_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('items', models.ManyToManyField(to='catalog.CartItem')),
            ],
        ),
    ]
