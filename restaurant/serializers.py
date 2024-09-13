from rest_framework import serializers
from .models import Restaurant, MenuItem, MenuCategory
from users.serializers import UserSerializer


class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)  # Format the datetime

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'status', 'total_sales', 'created_at', 'category_name', 'category']


# Menu category serializer
        
class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'restaurant', 'items']

# restaurant serializer
class RestaurantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_name', 'restaurant_location', 'user', 'categories', 'verified']