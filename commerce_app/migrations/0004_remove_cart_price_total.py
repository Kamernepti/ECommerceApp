# Generated by Django 3.1.7 on 2021-03-24 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce_app', '0003_auto_20210324_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='price_total',
        ),
    ]