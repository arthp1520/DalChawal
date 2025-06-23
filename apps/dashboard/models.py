
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    image = models.ImageField(upload_to="post_image/")
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField()
    is_active = models.BooleanField(default=True)

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, default="User", null=True, blank=True)
    mobile = models.CharField(max_length=14, unique=True)
    password = models.CharField(max_length=255)
    otp = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/',default="images\default-profile-icon.jpg", blank=True, null=True)
    
# ✅ Document model for file upload
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

