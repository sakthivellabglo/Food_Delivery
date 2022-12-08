from django.contrib import admin
from .models import Cart, Food, Order, Profile


admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Cart)
# Register your models here.
