# Generated by Django 3.2.7 on 2021-09-29 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_shipment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='is_finished',
        ),
        migrations.AddField(
            model_name='shipment',
            name='status',
            field=models.IntegerField(choices=[(0, 'Đợi tài xế xác nhận'), (1, 'Đợi tài xế nhận hàng'), (2, 'Đang vận chuyển'), (3, 'Đã giao hàng'), (4, 'Đã bị hủy')], default=1),
        ),
        migrations.AlterField(
            model_name='customerready',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='destinationinfo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='driveronline',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
