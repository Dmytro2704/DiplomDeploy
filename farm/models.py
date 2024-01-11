from django.contrib.auth.models import User
from django.db import models

LOCATION_CHOICES = (
    ('location1', 'Дніпро'),
    ('location2', 'Павлоград'),
    ('location3', 'Новомосковськ'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(default="login", max_length=150, verbose_name="Username")
    login = models.CharField(max_length=150, verbose_name="Login")
    password = models.CharField(max_length=150, verbose_name="Password")
    email = models.EmailField(max_length=100, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    date_of_birth = models.CharField(verbose_name="Date of birth")
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, verbose_name="Location")
    no_delivery = models.BooleanField(default=False)

    def __str__(self):
        return self.login


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.CharField(max_length=100, blank=True, null=True)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
