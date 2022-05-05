# Generated by Django 3.2 on 2022-05-05 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20220505_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('DELIVERED', 'DELIVERED'), ('ORDERED', 'ORDERED'), ('CANCELLED', 'CANCELLED')], max_length=255, null=True),
        ),
    ]
