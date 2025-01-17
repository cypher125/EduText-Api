from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Adds additional fields specific to the educational institution context:
    - role: Staff or Admin
    - department: Academic department
    - level: Academic level
    - matric_number: Student ID
    - phone_number: Contact number
    
    Note:
        Uses Django's built-in username and password fields from AbstractUser
    """
    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')
    department = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=10, blank=True)
    matric_number = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})" 