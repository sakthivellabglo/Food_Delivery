from django.db import models

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class FoodItem(models.Model):
    name = models.CharField(max_length=30)
    food_details = models.CharField(max_length=100)
    price = models.IntegerField()
    image =models.ImageField(upload_to='images')
    is_veg =models.BooleanField()
    is_available =models.BooleanField(default=False)

class Restaurant(models.Model):
    name = models.CharField(max_length=40)
    image =models.ImageField(upload_to='images')
    address = models.CharField(max_length=100)
    phone_number =models.IntegerField()
    foods = models.ManyToManyField(FoodItem)

    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    food = models.ManyToManyField(FoodItem)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_item =  models.ForeignKey(Menu,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    delivery_address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    order_time = models.DateTimeField(auto_now_add=True)

class Deliveryed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    is_delivered =models.BooleanField(default=False)
    delivery_time = models.DateTimeField(auto_now_add=True)



# Create your models here.
