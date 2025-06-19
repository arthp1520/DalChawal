from django.db import models

# Create your models here.


class Post(models.Model):
    image = models.ImageField(upload_to="post_image/")
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    


class User(models.Model):
    # name = models.CharField(max_length=100, blank=True, null=True)  # Optional but useful
    # enrollment = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)
    otp = models.IntegerField(null=True, blank=True)  # REQUIRED
    is_active = models.BooleanField(default=False)  # For OTP verification

