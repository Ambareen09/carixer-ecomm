# Generated by Django 3.2 on 2022-05-08 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_orderdetail_tracking_number_alter_orderdetail_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('DELIVERED', 'DELIVERED'), ('ORDERED', 'ORDERED'), ('CANCELLED', 'CANCELLED'), ('INCART', 'INCART')], max_length=255, null=True),
        ),
    ]
