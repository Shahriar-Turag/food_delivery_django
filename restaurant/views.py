from django.shortcuts import render
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Import AllowAny permission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound

import logging

logger = logging.getLogger(__name__)

from .models import Restaurant, MenuCategory, MenuItem
from .serializers import RestaurantSerializer, MenuCategorySerializer, MenuItemSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def list(self, request, *args, **kwargs):
        restaurant_id = request.query_params.get('id')
        verified = request.query_params.get('verified')

        queryset = self.get_queryset()

        # Filter by restaurant_id if it exists in the query parameters
        if restaurant_id:
            queryset = queryset.filter(id=restaurant_id)
        
        # Filter by verified status if provided in the query parameters
        if verified is not None:
            # Convert string to Boolean
            verified_bool = verified.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(verified=verified_bool)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Menu category viewset
class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

    def create(self, request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant')

        if not restaurant_id:
            raise ValidationError({"error": "Restaurant ID is required."})

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(restaurant=restaurant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        # Get the 'restaurant' query parameter
        restaurant_id = request.query_params.get('restaurant')
        
        queryset = self.get_queryset()

        # Filter by restaurant_id if it exists in the query parameters
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        category = self.get_object()  # Retrieves the category object
        category.name = request.data.get('name', category.name)  # Updates the name
        category.save()
        serializer = self.get_serializer(category)
        return Response(serializer.data)


# Menu item viewset
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def create(self, request, *args, **kwargs):
        category_id = request.data.get('category')
        category = MenuCategory.objects.get(id=category_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(category=category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Item deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()
