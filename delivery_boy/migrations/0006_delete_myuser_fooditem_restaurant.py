# Generated by Django 4.1.2 on 2022-11-26 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_boy', '0005_myuser_alter_deliveryboy_user_alter_order_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
        migrations.AddField(
            model_name='fooditem',
            name='restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery_boy.restaurant'),
            preserve_default=False,
        ),
    ]
