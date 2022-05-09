# Generated by Django 4.0.4 on 2022-05-09 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0025_remove_product_price_alter_orderdetail_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('INCART', 'INCART'), ('DELIVERED', 'DELIVERED'), ('ORDERED', 'ORDERED'), ('CANCELLED', 'CANCELLED')], max_length=255, null=True),
        ),
    ]
