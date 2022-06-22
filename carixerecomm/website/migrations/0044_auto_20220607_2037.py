# Generated by Django 3.2 on 2022-06-07 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0043_alter_orderdetail_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('WISHLIST', 'WISHLIST'), ('DELIVERED', 'DELIVERED'), ('INCART', 'INCART'), ('CANCELLED', 'CANCELLED'), ('INTRANSIT', 'INTRANSIT'), ('ORDERED', 'ORDERED')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='location',
            field=models.CharField(default='All', max_length=255),
        ),
    ]
