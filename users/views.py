from .models import User, Restaurant, Rider, Order, Consumer
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Import AllowAny permission
from rest_framework.exceptions import ValidationError
from .serializers import (
    UserSerializer,
    RiderSerializer,
    OrderSerializer,
    ConsumerSerializer,
    RestaurantRegistrationSerializer, 
    RiderRegistrationSerializer, 
    ConsumerRegistrationSerializer, 
    LoginSerializer,
   
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound

import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except User.DoesNotExist:
            raise NotFound(detail="User not found.", code=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class RiderViewSet(viewsets.ModelViewSet):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ConsumerViewSet(viewsets.ModelViewSet):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer

class RegisterRestaurantView(views.APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = RestaurantRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'user_type': user.user_type,
                'restaurant_name': user.restaurant.restaurant_name,
                'restaurant_location': user.restaurant.restaurant_location,
                'verified': user.restaurant.verified
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterRiderView(views.APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = RiderRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'user_type': user.user_type
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterConsumerView(views.APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = ConsumerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'user_type': user.user_type
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            # Base response data
            response_data = {
                'token': str(refresh.access_token),
                'user_info': {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'user_type': user.user_type,
                    'phone_number': user.phone_number,
                    'image': user.image.url if user.image else None
                }
            }

            # If the user is a restaurant, add restaurant-specific information
            if user.user_type == 'restaurant':
                try:
                    restaurant = Restaurant.objects.get(user=user)
                    response_data['user_info']['restaurant_id'] = restaurant.id
                    response_data['user_info']['restaurant_name'] = restaurant.restaurant_name
                    response_data['user_info']['restaurant_location'] = restaurant.restaurant_location
                    response_data['user_info']['verified'] = restaurant.verified
                except Restaurant.DoesNotExist:
                    response_data['user_info']['restaurant_id'] = None
                    response_data['user_info']['restaurant_name'] = None
                    response_data['user_info']['restaurant_location'] = None
                    response_data['user_info']['verified'] = None

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
