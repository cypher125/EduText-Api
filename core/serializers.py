from rest_framework import serializers
from .models import Textbook, Order, OrderItem

class TextbookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Textbook model.
    Handles conversion between Textbook instances and JSON representations.
    
    Note:
        price is configured to return as a number rather than string
    """
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    
    class Meta:
        model = Textbook
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    Handles conversion between OrderItem instances and JSON representations.
    
    Note:
        book_title and course_code are read-only fields populated from the textbook
    """
    book_title = serializers.CharField(read_only=True)
    course_code = serializers.CharField(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['textbook', 'quantity', 'price', 'book_title', 'course_code']

    def create(self, validated_data):
        """
        Override create to ensure book details are cached from the textbook.
        """
        textbook = validated_data['textbook']
        validated_data['book_title'] = textbook.title
        validated_data['course_code'] = textbook.course_code
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    Handles conversion between Order instances and JSON representations.
    
    Includes nested serialization of order items.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'reference', 'status', 'total_amount', 'items', 'created_at',
            'student_name', 'student_email', 'matric_number', 'department', 
            'level', 'phone_number'
        ]

    def create(self, validated_data):
        """
        Override create to handle nested creation of order items.
        """
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order 