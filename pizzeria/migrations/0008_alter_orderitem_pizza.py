# Generated by Django 4.2.3 on 2023-08-26 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0007_category_max_selection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='pizza',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzeria.pizza'),
        ),
    ]
