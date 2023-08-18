from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    PROFILE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    
    profile_type = models.CharField(max_length=10, choices=PROFILE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/')
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    groups = None
    user_permissions = None