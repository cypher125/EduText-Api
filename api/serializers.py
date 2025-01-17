from rest_framework import serializers
from .models import User, Department, Textbook, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'department', 'level', 'matric_number', 'phone_number')
        read_only_fields = ('id',)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class TextbookSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Textbook
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    textbook_title = serializers.CharField(source='textbook.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Order
        fields = '__all__' 