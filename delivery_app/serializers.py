from rest_framework import serializers
from django.contrib.auth.models import User

from delivery_app.models import FoodItem, Menu, Order, Restaurant

class CreateuserSerializers(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = ('id', 'username', 'password',
                   'email', 'first_name', 'last_name')
         write_only_fields = ('password',)
         read_only_fields = ('id',)
     def create(self, validated_data):
         user = User.objects.create_superuser(
             username=validated_data['username'],
             email=validated_data['email'],
             first_name=validated_data['first_name'],
             last_name=validated_data['last_name'],

         )

         user.set_password(validated_data['password'])
         user.save()
         return user




class Loginserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class Menuserializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['restaurant', 'food']

class Foodserializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['name', 'food_details','price','image']

class Resserializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'image','address','phone_number','foods']


class Orderserializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id','user', 'order_item','price','delivery_address','pincode','order_time','quantity']
        read_only_fields = ('id', 'user','order_time','price')

class Foodserializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['name', 'food_details','price','image','restaurant']