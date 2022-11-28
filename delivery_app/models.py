from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image =models.ImageField(upload_to="images")
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField( max_length=10, blank=True)
    city = models.CharField(max_length=255)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Restaurant(models.Model):
    manager = models.OneToOneField(User, on_delete=models.RESTRICT)
    image =models.ImageField(upload_to="images")
    name = models.CharField(max_length=255, blank=False, null=False)
    food_type = models.CharField(max_length=255, blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=1024, blank=False, null=False)
    open_time = models.TimeField(blank=False, null=False)
    close_time = models.TimeField(blank=False, null=False)

    def __str__(self):
        return "<{}: {}>".format(self.pk, self.name)


class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, blank=False, null=False)
    image =models.ImageField(upload_to="images")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    is_organic = models.BooleanField(default=False, blank=False, null=False)
    is_vegan = models.BooleanField(default=False, blank=False, null=False)
    def __str__(self):
        return  self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    foods = models.ManyToManyField(Food)
    total_price =models.PositiveIntegerField()
    is_accepted = models.BooleanField(default=False, blank=False, null=False)
    is_cancelled = models.BooleanField(default=False, blank=False, null=False)
    is_delivered = models.BooleanField(default=False, blank=False, null=False)
    create_datetime = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    accept_datetime = models.DateTimeField(default=None, null=True, blank=True)
    cancell_datetime = models.DateTimeField(default=None, null=True, blank=True)
    delivered_datetime = models.DateTimeField(default=None, null=True, blank=True)
    note = models.CharField(max_length=1024, default="")
    
