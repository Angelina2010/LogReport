# Generated by Django 2.2.1 on 2019-05-05 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20190504_2230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='buying_type',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
    ]