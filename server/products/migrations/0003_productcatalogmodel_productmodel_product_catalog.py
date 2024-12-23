# Generated by Django 4.2.16 on 2024-11-20 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productmodel_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCatalogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='productmodel',
            name='product_catalog',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_catalog', to='products.productcatalogmodel'),
        ),
    ]
