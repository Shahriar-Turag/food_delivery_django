from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, MenuCategoryViewSet, MenuItemViewSet


router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'categories', MenuCategoryViewSet)
router.register(r'items', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
