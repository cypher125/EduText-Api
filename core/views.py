from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import Textbook, Order
from .serializers import TextbookSerializer, OrderSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

@extend_schema(tags=['textbooks'])
class TextbookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing textbooks.
    
    Provides CRUD operations for textbooks and additional endpoints for filtering.
    Allows unauthenticated access for read operations.
    """
    queryset = Textbook.objects.all()
    serializer_class = TextbookSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def filters(self, request):
        """
        Get available filter options for textbooks.
        
        Returns:
            dict: Available departments and levels for filtering
        """
        departments = [choice[1] for choice in Textbook.DEPARTMENT_CHOICES]
        levels = [choice[1] for choice in Textbook.LEVEL_CHOICES]
        
        return Response({
            'departments': departments,
            'levels': levels
        })

    @extend_schema(
        parameters=[
            OpenApiParameter(name='department', description='Filter by department', required=False, type=str),
            OpenApiParameter(name='level', description='Filter by level', required=False, type=str),
            OpenApiParameter(name='search', description='Search in title and course code', required=False, type=str),
        ]
    )
    def get_queryset(self):
        """
        Get filtered queryset of textbooks based on query parameters.
        
        Filters:
            department: Filter by academic department
            level: Filter by academic level
            search: Search in title and course code
        """
        queryset = Textbook.objects.all()
        department = self.request.query_params.get('department', None)
        level = self.request.query_params.get('level', None)
        search = self.request.query_params.get('search', None)

        if department and department != "All Departments":
            department_value = next((choice[0] for choice in Textbook.DEPARTMENT_CHOICES 
                                  if choice[1] == department), None)
            if department_value:
                queryset = queryset.filter(department=department_value)
                
        if level and level != "All Levels":
            level_value = next((choice[0] for choice in Textbook.LEVEL_CHOICES 
                              if choice[1] == level), None)
            if level_value:
                queryset = queryset.filter(level=level_value)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(course_code__icontains=search)
            )
        
        return queryset

@extend_schema(tags=['orders'])
class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders.
    
    Provides CRUD operations for orders with special handling for:
    - Stock validation and updates
    - Nested order item creation
    - Staff-only access to all orders
    """
    serializer_class = OrderSerializer
    permission_classes = []
    lookup_field = 'reference'
    lookup_url_kwarg = 'reference'
    queryset = Order.objects.all()

    def get_queryset(self):
        """
        Get orders queryset based on user permissions.
        Staff can see all orders, others can see their own orders.
        """
        queryset = Order.objects.all()
        if not self.request.user.is_staff:
            # Allow users to view their own orders by reference
            reference = self.kwargs.get('reference')
            if reference:
                return queryset.filter(reference=reference)
            return Order.objects.none()
        return queryset

    def perform_create(self, serializer):
        """
        Create order with atomic transaction handling.
        
        Validates stock availability and updates stock levels
        for all items in the order.
        
        Raises:
            ValidationError: If insufficient stock for any item
        """
        items_data = self.request.data.get('items', [])
        
        with transaction.atomic():
            # First validate stock for all items
            for item in items_data:
                textbook = Textbook.objects.select_for_update().get(id=item['textbook'])
                if textbook.stock < item['quantity']:
                    raise serializers.ValidationError({
                        'detail': f"Insufficient stock for {textbook.title}. Only {textbook.stock} available."
                    })

            # If all stock checks pass, create order and update stock
            order = serializer.save()
            
            for item in items_data:
                textbook = Textbook.objects.select_for_update().get(id=item['textbook'])
                textbook.stock -= item['quantity']
                textbook.save()

    def create(self, request, *args, **kwargs):
        """
        Create order with debug logging.
        """
        try:
            print("Received order data:", request.data)  # Debug log
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print("Order creation error:", str(e))  # Debug log
            raise
