# Generated by Django 4.2.16 on 2024-11-26 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_customerordermodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerordermodel',
            name='status',
            field=models.CharField(blank=True, choices=[('Order', 'Order'), ('Purchased', 'Purchased'), ('Pending', 'Pending'), ('returned', 'returned'), ('Complete', 'Complete'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Oder', max_length=1000, null=True),
        ),
    ]