from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=60, verbose_name="Email")
    password = models.CharField(max_length=128, verbose_name="Password")
    name = models.CharField(max_length=100, verbose_name="Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")
    subscription = models.BooleanField(default=False, verbose_name="Subscription")

    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = CustomUserManager()

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")


    def __str__(self):
        return self.email
    

class Partner(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=128, verbose_name="Password")
    establishment_name = models.CharField(max_length=100, verbose_name="Establishment Name")
    location = models.CharField(max_length=100, verbose_name="Location")
    description = models.TextField(verbose_name="Description")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.establishment_name




