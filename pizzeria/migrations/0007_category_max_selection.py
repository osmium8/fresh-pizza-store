# Generated by Django 4.2.3 on 2023-08-26 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0006_remove_item_category_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='max_selection',
            field=models.SmallIntegerField(null=True),
        ),
    ]
