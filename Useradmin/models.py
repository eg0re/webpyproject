from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
