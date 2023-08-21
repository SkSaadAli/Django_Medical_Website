from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
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

    def __str__(self):
        return self.username

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Blog Model
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    blog_picture = models.ImageField(upload_to='blog_pics/' , default='user_auth/default_images/default-blog-image.png')
    content = models.TextField(null=True, blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        words = self.content.split()[:15]
        return ' '.join(words)

        

