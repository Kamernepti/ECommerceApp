# Generated by Django 3.1.7 on 2021-04-01 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce_app', '0006_remove_cart_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='name',
        ),
    ]