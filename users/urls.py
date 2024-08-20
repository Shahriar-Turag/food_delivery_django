from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, RestaurantViewSet, RiderViewSet, OrderViewSet, ConsumerViewSet,
    RegisterRestaurantView, RegisterRiderView, RegisterConsumerView, LoginView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'riders', RiderViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'consumers', ConsumerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/restaurant/', RegisterRestaurantView.as_view(), name='register_restaurant'),
    path('register/rider/', RegisterRiderView.as_view(), name='register_rider'),
    path('register/consumer/', RegisterConsumerView.as_view(), name='register_consumer'),
    path('login/', LoginView.as_view(), name='login'),
]
