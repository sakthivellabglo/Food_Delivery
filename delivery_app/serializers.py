from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Cart, Profile, Restaurant, Food, Order


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",)

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id","birth_date", "gender", "phone_number", "address","city", "is_manager","is_approved")
        extra_kwargs = {
            "is_approved": {"read_only": True},
            "id": {"read_only": True},
            "is_manager": {"read_only": True},
            "birth_date": {"read_only": True}}

class MangerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("birth_date", "gender", "phone_number", "city", "address","is_manager","is_approved")
        extra_kwargs = {
            "is_approved": {"read_only": True},}

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ( 
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "profile",
        )
        extra_kwargs = {"id": {"read_only": True},}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        user = User.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile")
        profile = instance.profile
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.set_password(validated_data.get("password"))
        profile.gender = profile_data.get("gender", profile.gender)
        profile.phone_number = profile_data.get("phone_number", profile.phone_number)
        profile.address = profile_data.get("address", profile.address)
        profile.city = profile_data.get("city", profile.city)
        instance.save()
        profile.save()

        return instance

class ManagerSerializer(serializers.ModelSerializer):
    profile = MangerProfileSerializer()

    class Meta:
        model = User
        fields = ( 
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "profile",
        )
        extra_kwargs = {"id": {"read_only": True},}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        user = User.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile")
        profile = instance.profile
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.set_password(validated_data.get("password"))
        profile.birth_date = profile_data.get("birth_date", profile.birth_date)
        profile.gender = profile_data.get("gender", profile.gender)
        profile.phone_number = profile_data.get("phone_number", profile.phone_number)
        profile.city = profile_data.get("city", profile.city)
        profile.is_manager = profile_data.get("is_manager", profile.is_manager)
        instance.save()
        profile.save()

        return instance

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
        extra_kwargs = {"manager": {"read_only": True}}


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"
        extra_kwargs = {"restaurant": {"read_only": True}}

class CartSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='food.name',read_only=True)
    resname = serializers.CharField(source='food.restaurant',read_only=True)
    class Meta:
        model = Cart
        fields = ["id","food","quantity","name","resname","price"]
        extra_kwargs = {"customer": {"read_only": True},
                        "price": {"read_only": True},}
        


class PlaceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {
            "order_price": {"read_only": True},
            "customer": {"read_only": True},
            "is_accepted": {"read_only": True},
            "is_cancelled": {"read_only": True},
            "is_delivered": {"read_only": True},
            "accept_datetime": {"read_only": True},
            "cancell_datetime": {"read_only": True},
            "delivered_datetime": {"read_only": True},
            "time_to_deliver": {"read_only": True},
            "total_price":{"read_only":True}
        }

    def validate(self, data):
        """
        Check all ordered foods to be from one restaurants.
        """
        food_list = data["cart"]
        print(food_list[0].food)
        restaurant_id = food_list[0].food.restaurant.id
        print(restaurant_id)
        for food in food_list:
            if food.food.restaurant.id != restaurant_id:
                raise serializers.ValidationError(
                    "All ordered foods should be from one restaurant."
                )
        return data


class CancellOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("is_cancelled",)


class ApproveDeliveredOrderSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Order
        fields = ("is_delivered",)


class AcceptOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("is_accepted",)

class AdminApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("is_approved",)