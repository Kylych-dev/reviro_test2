from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager




class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('partner', 'Partner'),
        ('regularuser', 'RegularUser'),
    )
    email = models.EmailField(unique=True, max_length=60, verbose_name="Email")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)


    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")


    def __str__(self):
        return self.email


class RegularUser(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        primary_key=True
        )
    name = models.CharField(max_length=100, verbose_name="Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    subscription = models.BooleanField(default=False, verbose_name="Subscription")

    class Meta:
        verbose_name = "RegularUser"
        verbose_name_plural = "RegularUsers"    

    def __str__(self):
        return self.name


class Partner(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        primary_key=True
        )
    establishment_name = models.CharField(max_length=100, verbose_name="Establishment Name")
    location = models.CharField(max_length=100, verbose_name="Location")
    description = models.TextField(verbose_name="Description")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")


    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.establishment_name
    








'''
Partner
{
    "user": {
        "email": "jhn_cena@test.com",
        "role": "partner",
        "password": "secretpassword"
    },
    "establishment_name": "required",
    "location": "Trequired",
    "description": "This field",
    "phone_number": "Tis required"
}


RegularUser
{
    "user": {
        "email": "jhn_ce@test.com",
        "role": "regularuser",
        "password": "secretpassword"
    },
    "name": "required",
    "date_of_birth": "1990-01-01",
    "subscription": true
}
'''



















'''

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
    

class Partner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=128, verbose_name="Password")
    establishment_name = models.CharField(max_length=100, verbose_name="Establishment Name")
    location = models.CharField(max_length=100, verbose_name="Location")
    description = models.TextField(verbose_name="Description")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")





class RegularUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    subscription = models.BooleanField(default=False, verbose_name="Subscription")

   
'''