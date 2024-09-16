# Generated by Django 5.0.6 on 2024-07-07 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_product_cost_price_alter_product_selling_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bill_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='billitems',
            name='net_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='billitems',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
