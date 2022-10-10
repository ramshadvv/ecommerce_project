from django.db import models

# Create your models here.

class Trial(models.Model):
    first_name = models.CharField(max_length=50, null = True)
    last_name = models.CharField(max_length=50, null = True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True,max_length=255)
    phone = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)

