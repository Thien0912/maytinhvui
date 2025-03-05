# Generated by Django 5.1.6 on 2025-03-05 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_offer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutinfo',
            name='status',
            field=models.CharField(choices=[('unpaid', 'Chưa thanh toán'), ('pending', 'Đang xử lý'), ('shipped', 'Đã giao hàng'), ('cancelled', 'Đã hủy')], default='unpaid', max_length=20),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app.product'),
        ),
    ]
