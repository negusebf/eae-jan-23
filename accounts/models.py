from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.conf import settings

# Create your models here.

class User(AbstractUser, PermissionsMixin):
    address = models.CharField(max_length=100, null=True)
    def __str__(self):
        return "@{}".format(self.username)