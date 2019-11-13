from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=30)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',
    ]

    def __str__(self):
        return "{}".format(self.email)
        
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    photo = models.ImageField(upload_to='uploads', blank=True)

class ProtectedObject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    size = models.CharField(max_length=250, default="")
    photo = models.FileField(upload_to = 'img/', default = 'img/None/no-img.jpg')
    
class DetourPath(models.Model):  
   id = models.AutoField(primary_key=True)
   name = models.CharField(max_length=250)
   description = models.TextField()
   length = models.DecimalField(max_length=None, decimal_places=2, max_digits=19)
   protectedobject = models.ForeignKey(ProtectedObject, related_name='detour_paths', on_delete=models.CASCADE, null=True)
   
class Robot(models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    detection_algorithm = models.CharField(max_length=250)
    price = models.DecimalField(max_length=250, decimal_places=2, max_digits=19) 
    protectedobject = models.ForeignKey(ProtectedObject, related_name='robots', on_delete=models.CASCADE, null=True)


class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    sensor_type = models.CharField(max_length=250)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    lat = models.FloatField(blank=True)
    lng = models.FloatField(blank=True)
    measurement_value = models.FloatField(blank=True)

