# Generated by Django 5.1.6 on 2025-03-04 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_delete_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippinginfo',
            name='address',
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='phone_number',
        ),
    ]
