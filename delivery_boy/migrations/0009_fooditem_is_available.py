# Generated by Django 4.1.2 on 2022-11-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_boy', '0008_remove_fooditem_restaurant_restaurant_foods'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]