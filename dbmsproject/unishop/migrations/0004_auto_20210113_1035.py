# Generated by Django 3.0.3 on 2021-01-13 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unishop', '0003_auto_20210113_1033'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='bill',
            table='Bill',
        ),
        migrations.AlterModelTable(
            name='cartitem',
            table='CartItem',
        ),
        migrations.AlterModelTable(
            name='product',
            table='Product',
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='UserProfile',
        ),
    ]
