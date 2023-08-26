# Generated by Django 4.2.3 on 2023-08-26 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0009_rename_max_selection_category_required_amount'),
        ('audit', '0004_alter_orderedpizza_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedpizza',
            name='pizza',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pizzeria.pizza'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='track',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='audit.ordertrackhistory'),
        ),
        migrations.AlterField(
            model_name='ordertrackhistory',
            name='status',
            field=models.CharField(choices=[('PLACED', 'PLACED'), ('ACCEPTED', 'ACCEPTED'), ('PREPARING', 'PREPARING'), ('DISPATCHED', 'DISPATCHED'), ('DELIVERED', 'DELIVERED')], default='PLACED', max_length=15),
        ),
    ]