# Generated by Django 4.1.2 on 2022-11-26 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_boy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.AddField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(default='image.jpg', upload_to='images'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(default='fghh', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(default='image.jpg', upload_to='images'),
            preserve_default=False,
        ),
    ]