# Generated by Django 4.2.3 on 2023-08-26 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0005_orderitem_unique_pizza'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category_code',
        ),
    ]
