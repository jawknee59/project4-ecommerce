# Generated by Django 4.1.7 on 2023-03-08 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_remove_cart_items_remove_cart_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_url',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]