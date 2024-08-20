from django.contrib import admin
from .models import User, Restaurant, Rider, Order, Consumer

# Register your models here.

admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Rider)
admin.site.register(Order)
admin.site.register(Consumer)
