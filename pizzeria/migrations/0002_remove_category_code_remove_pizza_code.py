# Generated by Django 4.2.3 on 2023-08-26 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='code',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='code',
        ),
    ]
