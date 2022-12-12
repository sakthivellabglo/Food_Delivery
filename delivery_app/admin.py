from django.contrib import admin
from .models import Cart, Food, Order, Profile, Restaurant


admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Restaurant)
# Register your models here.
