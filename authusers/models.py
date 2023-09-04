from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
# Create your models here.



class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=15,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    # def catgory_image(self):
    #     return mark_safe('<img src="%s" width= "50px" height = "50px">' %(self.image.url))  # Corrected