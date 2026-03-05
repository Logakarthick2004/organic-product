from django.db import models
from django.conf import settings # To refer to your Custom User model


class User(models.Model):

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('store', 'Store'),
    )

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=150, unique=True)
    photo = models.FileField(upload_to='users/', blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
class Products(models.Model):
    # This links the product to a specific Store Owner ID
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # ... other fields
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50) # kg, ltr, etc.
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"
