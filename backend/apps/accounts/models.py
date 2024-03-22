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
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")

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
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")


    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.establishment_name
    








'''
Partner register
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


RegularUser register
{
    "user": {
        "email": "user@mail.ru",
        "role": "regularuser",
        "password": 1
    },
    "name": "required",
    "date_of_birth": "1990-01-01",
    "subscription": true
}



User login
{
    "email": "user@mail.ru",
    "password": 1
}

http://127.0.0.1:3000/api/v1/login/

http://127.0.0.1:3000/api/v1/login/?token= 





"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExMTAyMDM3LCJpYXQiOjE3MTEwOTg0MzcsImp0aSI6IjlkYzVkNjhjODc5ZTQ4OGM4ZWYxY2MzNDJkMzM5NjdiIiwidXNlcl9pZCI6Mn0.0KV6fAavBw-79iy2FA1TuMV20J8yU9Nk7t5rQmxTVfk"
















 File "/home/m/Desktop/practice/reviro_test2/env/lib/python3.11/site-packages/django/db/models/fields/related_descriptors.py", line 524, in __get__
    raise self.RelatedObjectDoesNotExist(
apps.accounts.models.CustomUser.partner.RelatedObjectDoesNotExist: CustomUser has no partner.
[22/Mar/2024 10:45:02] "PUT /api/v1/partner_update/1/ HTTP/1.1" 500 110467


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('partner', 'Partner'),
        ('regularuser', 'RegularUser'),
    )
    email = models.EmailField(unique=True, max_length=60, verbose_name="Email")
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class RegularUser(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        primary_key=True
        )
    name = models.CharField(max_length=100, verbose_name="Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    subscription = models.BooleanField(default=False, verbose_name="Subscription")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")

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
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role']
        read_only_fields = ['id']

class RegularUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = RegularUser
        fields = ['user', 'name', 'date_of_birth', 'subscription']

class PartnerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Partner
        # fields = ['user', 'name', 'date_of_birth', 'subscription']
        fields = '__all__'



class PartnerUpdateView(generics.UpdateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.partner
    

    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_data = request.data.pop('user', {})  # Extract user data from request
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Update user object if email is provided
        if user_data.get('email'):
            custom_user = instance.user
            custom_user.email = user_data['email']
            custom_user.save()

        return Response(serializer.data)
    
    
    
    







'''


