from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager  # Import the custom user manager

# Custom User model
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager  # Import your custom user manager
from django.utils import timezone
from restaurant.models import Restaurant

class User(AbstractUser):
    USER_TYPES = (
        ('restaurant', 'Restaurant'),
        ('rider', 'Rider'),
        ('consumer', 'Consumer'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=150, blank=True, null=True, unique=False)  # Allow username to be blank
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type', 'password']

    def __str__(self):
        return self.email
  

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
    placed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Order {self.id} - {self.status}'

# Consumer model
class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email  # Returns the user's email instead of username
