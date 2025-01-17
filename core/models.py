from django.db import models
from django.conf import settings

class Department(models.Model):
    """
    Model representing academic departments in the institution.
    
    Attributes:
        name (str): Full name of the department
        code (str): Short code/abbreviation for the department
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Textbook(models.Model):
    """
    Model representing academic textbooks available in the system.
    
    Attributes:
        title (str): Title of the textbook
        course_code (str): Course code the textbook is used for
        department (str): Department the textbook belongs to
        level (str): Academic level the textbook is intended for
        price (decimal): Price of the textbook
        description (str): Brief description of the textbook
        stock (int): Current available quantity
        image (ImageField): Cover image of the textbook
        is_popular (bool): Whether the textbook is marked as popular
        is_new (bool): Whether the textbook is marked as new
        created_at (datetime): When the textbook was added
        updated_at (datetime): When the textbook was last updated
    """
    title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20)
    DEPARTMENT_CHOICES = (
        ('computer_science', 'Computer Science'),
        ('computer_engineering', 'Computer Engineering'),
        ('civil_engineering', 'Civil Engineering'),
        ('electrical_engineering', 'Electrical Engineering'),
        ('mechanical_engineering', 'Mechanical Engineering'),
        ('chemical_engineering', 'Chemical Engineering'),
        ('science_laboratory', 'Science Laboratory Technology'),
        ('food_technology', 'Food Technology'),
        ('accountancy', 'Accountancy'),
        ('business_admin', 'Business Administration'),
        ('marketing', 'Marketing'),
        ('mass_comm', 'Mass Communication'),
    )
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    LEVEL_CHOICES = (
        ('nd1', 'ND 1'),
        ('nd2', 'ND 2'),
        ('hnd1', 'HND 1'),
        ('hnd2', 'HND 2'),
    )
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=179)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='textbooks/', null=True, blank=True)
    is_popular = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.course_code})"

class Order(models.Model):
    """
    Model representing customer orders for textbooks.
    
    Attributes:
        reference (str): Unique reference number for the order
        status (str): Current status of the order (pending/completed/failed)
        total_amount (decimal): Total cost of the order
        created_at (datetime): When the order was placed
        student_name (str): Name of the student placing the order
        student_email (str): Email of the student
        matric_number (str): Student's matriculation number
        department (str): Student's department
        level (str): Student's academic level
        phone_number (str): Student's contact number
    """
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Student information fields
    student_name = models.CharField(max_length=200)
    student_email = models.EmailField()
    matric_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Order {self.reference} by {self.student_name}"

class OrderItem(models.Model):
    """
    Model representing individual items within an order.
    
    Attributes:
        order (Order): The parent order this item belongs to
        textbook (Textbook): The textbook being ordered
        quantity (int): Number of copies ordered
        price (decimal): Price per unit at time of order
        book_title (str): Cached title of the textbook
        course_code (str): Cached course code of the textbook
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Cache book details for order history
    book_title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.quantity}x {self.book_title}"
    
    def save(self, *args, **kwargs):
        """Override save to cache book details"""
        if not self.book_title:
            self.book_title = self.textbook.title
        if not self.course_code:
            self.course_code = self.textbook.course_code
        super().save(*args, **kwargs) 