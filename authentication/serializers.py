from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Handles basic user information including custom fields
    for educational institution context.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'role', 'department', 'level', 'matric_number', 'phone_number')
        read_only_fields = ('id',)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that includes user data in response.
    """
    def validate(self, attrs):
        """
        Add user data to token response.
        """
        data = super().validate(attrs)
        user = self.user
        data['user'] = UserSerializer(user).data
        return data

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles creation of new user accounts with all required fields
    including password handling.
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                 'role', 'department', 'level', 'matric_number', 'phone_number')

    def create(self, validated_data):
        """
        Create new user with proper password hashing.
        """
        user = User.objects.create_user(**validated_data)
        return user 