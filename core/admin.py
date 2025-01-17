from django.contrib import admin
from .models import Textbook, Order, OrderItem

@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Textbook model.
    Customizes how textbooks are displayed and managed in the admin interface.
    """
    list_display = ('title', 'department', 'level', 'price')
    list_filter = ('department', 'level')
    search_fields = ('title', 'department')
    ordering = ('title',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for OrderItem model.
    Customizes how order items are displayed and managed in the admin interface.
    """
    list_display = ('order', 'textbook', 'quantity', 'price')
    list_filter = ('order__status',)
    search_fields = ('order__reference', 'textbook__title')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model.
    Customizes how orders are displayed and managed in the admin interface.
    """
    list_display = ('reference', 'student_name', 'matric_number', 'department', 'level', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'department', 'level', 'created_at')
    search_fields = ('reference', 'student_name', 'student_email', 'matric_number')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
