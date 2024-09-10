from rest_framework import serializers
from .models import User, Restaurant, Rider, Consumer, Order, MenuItem, MenuCategory

# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'user_type', 'phone_number', 'image']

# menu item serializer
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

# rider serializer
class RiderSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use the UserSerializer to nest user details
    class Meta:
        model = Rider
        fields = ['id', 'user']

# order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

# consumer serializer
class ConsumerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use the UserSerializer to nest user details
    class Meta:
        model = Consumer
        fields = ['id', 'user']


# restaurant registration serializer
class RestaurantRegistrationSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(write_only=True)  # Explicitly add this field for input only
    restaurant_location = serializers.CharField(write_only=True)  # Explicitly add this field for input only
    verified = serializers.BooleanField(read_only=True)  # Set verified to True by default

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'user_type', 'restaurant_name', 'restaurant_location', 'verified', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract restaurant-specific data
        restaurant_name = validated_data.pop('restaurant_name')
        restaurant_location = validated_data.pop('restaurant_location')
        
        # Set the user type to 'restaurant'
        validated_data['user_type'] = 'restaurant'
        
        # Create the User
        user = User.objects.create_user(**validated_data)
        
        # Create the associated Restaurant
        Restaurant.objects.create(user=user, restaurant_name=restaurant_name, restaurant_location=restaurant_location)
        
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            # Add restaurant_name and restaurant_location if it's a restaurant user
            restaurant = Restaurant.objects.get(user=instance)
            representation['restaurant_name'] = restaurant.restaurant_name
            representation['restaurant_location'] = restaurant.restaurant_location
            representation['verified'] = restaurant.verified
        except Restaurant.DoesNotExist:
            pass  # Skip adding restaurant_name and restaurant_location if not available
        return representation

# rider registration serializer
class RiderRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['user_type'] = 'rider'  # Ensure user_type is set to 'rider'
        user = User.objects.create_user(**validated_data)
        Rider.objects.create(user=user)  # Create associated Rider
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation  # Only return the fields defined in Meta

# consumer registration serializer
class ConsumerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['user_type'] = 'consumer'  # Ensure user_type is set to 'consumer'
        user = User.objects.create_user(**validated_data)
        Consumer.objects.create(user=user)  # Create associated Consumer
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation  # Only return the fields defined in Meta

# login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email and password:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError('Incorrect credentials')
            return user
        raise serializers.ValidationError('Must provide both email and password')