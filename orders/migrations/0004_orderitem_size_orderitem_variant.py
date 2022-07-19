# Generated by Django 4.0.4 on 2022-07-18 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_is_delivered_order_is_processing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Product Size'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='variant',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Product Variant'),
        ),
    ]
