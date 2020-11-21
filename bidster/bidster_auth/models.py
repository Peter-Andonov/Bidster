from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    profile_pic = models.ImageField(upload_to='profiles')
    location = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)