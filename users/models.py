from django.db import models

# Create your models here.

class Users(models.Model):
    account = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=64, blank=True)
    
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=32, blank=True)
    age = models.IntegerField(default=0)
    phone_numer = models.CharField(max_length=11, blank=True)

    open_id = models.CharField(max_length=256, default='', blank=True)

    def __str__(self):
        return self.name

