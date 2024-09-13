from django.db import models


# Restaurant model
class Restaurant(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    restaurant_location = models.CharField(max_length=255)  
    verified = models.BooleanField(default=False)

    def __str__(self):
        return  self.restaurant_name  

# Menu category model
    
class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
# Menu item model
from django.db import models
from django.utils import timezone

class MenuItem(models.Model):
    STATUS_TYPES = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('draft', 'Draft'),
    )
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_TYPES, default='active')
    total_sales = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    category_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
