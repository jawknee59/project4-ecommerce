# Generated by Django 4.1.7 on 2023-03-13 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_cartitem_stripe_price_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='stripe_price_id',
        ),
    ]
