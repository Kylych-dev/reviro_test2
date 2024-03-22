from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework import generics, permissions


from apps.accounts.models import RegularUser, Partner
from .serializers import RegularUserSerializer, PartnerSerializer


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404



class RegularUserUpdateView(generics.UpdateAPIView):
    queryset = RegularUser.objects.all()
    serializer_class = RegularUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        regular_user_id = self.kwargs.get('pk')
        return RegularUser.objects.get(pk=regular_user_id)
    

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
    
class PartnerUpdateView(generics.UpdateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        partner_id = self.kwargs.get('pk')
        return Partner.objects.get(pk=partner_id)
    

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

Теперь, когда вы отправляете запрос на обновление с данными, например:

{
    "user": {
        "email": "new_email@example.com"
    },
    "name": "user",
    "date_of_birth": "2000-01-01",
    "subscription": true
}



update 

    {
        "user": {
            "email": "new_email@example.com"
        },
        "name": "new_user",
        "date_of_birth": "2005-01-01",
        "subscription": true
    }

    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

'''












'''

from rest_framework import serializers
from apps.accounts.models import RegularUser, CustomUser




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'avatar', 'role']  

class RegularUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=True)

    class Meta:
        model = RegularUser
        fields = ['user', 'name', 'date_of_birth', 'subscription']

        


class RegularUserUpdateView(generics.UpdateAPIView):
    queryset = RegularUser.objects.all()
    serializer_class = RegularUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.regularuser

    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



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


class RegularUser(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        primary_key=True
        )
    name = models.CharField(max_length=100, verbose_name="Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    subscription = models.BooleanField(default=False, verbose_name="Subscription")



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

{
    "name": "user0",
    "date_of_birth": "2000-01-01",
    "subscription": true
}


{
    "user": [
        "This field is required."
    ]
}






'''



























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

update 

{
    "user": {
        "email": "user0@mail.ru",
        "role": "regularuser",
        "password": 12
    },
    "name": "user0",
    "date_of_birth": "2000-01-01",
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
'''




    # def update_detail(self, request, *args, **kwargs):
    #     try:
    #         user = self.queryset.get(phone_number=kwargs.get("phone_number"))
    #         serializer = RegularUserSerializer(user, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except RegularUser.DoesNotExist as ex:
    #         # logger.warning(
    #         #     f"При изменении пользователь не найден",
    #         #     extra={
    #         #         "Exception": ex,
    #         #         "error_code": f"{__class__.__name__}.{self.action}",
    #         #     },
    #         # )
    #         return Response(
    #             {"Сообщение": "При изменении пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
    #         )