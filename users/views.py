from .models import User, Restaurant, Rider, Order, Consumer, MenuCategory, MenuItem
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Import AllowAny permission
from .serializers import (
    UserSerializer,
    RestaurantSerializer,
    RiderSerializer,
    OrderSerializer,
    ConsumerSerializer,
    RestaurantRegistrationSerializer, 
    RiderRegistrationSerializer, 
    ConsumerRegistrationSerializer, 
    LoginSerializer,
    MenuCategorySerializer,
    MenuItemSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

# Menu category viewset
class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

    def create(self, request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(restaurant=restaurant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
                'restaurant_location': user.restaurant.restaurant_location
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
                    'user_type': user.user_type
                }
            }

            # If the user is a restaurant, add restaurant-specific information
            if user.user_type == 'restaurant':
                try:
                    restaurant = Restaurant.objects.get(user=user)
                    response_data['user_info']['restaurant_name'] = restaurant.restaurant_name
                    response_data['user_info']['restaurant_location'] = restaurant.restaurant_location
                except Restaurant.DoesNotExist:
                    response_data['user_info']['restaurant_name'] = None
                    response_data['user_info']['restaurant_location'] = None

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
