# Generated by Django 3.0.3 on 2021-01-13 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unishop', '0005_auto_20210113_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_name',
            field=models.CharField(default='/static/unishop/images/new.webp', max_length=100),
            preserve_default=False,
        ),
    ]
