from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager  # Import the custom user manager

# Custom User model
class User(AbstractUser):
    USER_TYPES = (
        ('restaurant', 'Restaurant'),
        ('rider', 'Rider'),
        ('consumer', 'Consumer'),
        ('admin', 'Admin'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    objects = CustomUserManager()


    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type', 'password']

    def __str__(self):
        return self.email

# Restaurant model
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)  # This corresponds to restaurant_name in registration
    restaurant_location = models.CharField(max_length=255)  # This corresponds to restaurant_location in registration

    def __str__(self):
        return  self.restaurant_name  # Returns the restaurant name instead of username

# Menu category model
    
class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
# Menu item model
class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Rider model
class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email  # Returns the user's email instead of username

# Order model
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    consumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    rider = models.ForeignKey(Rider, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.status}'

# Consumer model
class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email  # Returns the user's email instead of username
