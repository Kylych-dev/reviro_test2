from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView


from apps.accounts.models import (
    RegularUser, 
    Partner, 
    CustomUser,
    ChatMessage
    )
from .serializers import (
    RegularUserSerializer, 
    PartnerSerializer, 
    ChatMessageSerializer
    )

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404



class RegularUserUpdateView(generics.UpdateAPIView):
    queryset = RegularUser.objects.all()
    serializer_class = RegularUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        regular_user_id = self.kwargs.get('pk')
        try:
            return RegularUser.objects.get(pk=regular_user_id)
        except RegularUser.DoesNotExist:
            return Response({'message': 'RegularUser not found'}, status=status.HTTP_404_NOT_FOUND)
    
    

    @swagger_auto_schema(
        method="put",
        operation_description="Обновление профиля обычного пользователя",
        operation_summary="Обновление профиля обычного пользователя",
        operation_id="update_regular_user_profile",
        tags=["Обычный пользователь"],
        responses={
            200: openapi.Response(description="OK - Профиль пользователя успешно обновлен"),
            201: openapi.Response(description="Created - Профиль пользователя успешно обновлен"),
            400: openapi.Response(description="Bad Request - Неверный запрос или некорректные данные"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            403: openapi.Response(description="Forbidden - Доступ запрещен"),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user.id != request.user.id:
            return Response(
                {
                    'message': 'You are not allowed to update this profile.'
                    }, 
                status=403
                )
        user_data = request.data.pop('user', {})  # Извлечение данных пользователя из запроса
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
        try:
            return Partner.objects.get(pk=partner_id)
        except Partner.DoesNotExist:
            return Response(
                {
                    'message': 'Partner not found'
                    }, 
                    status=status.HTTP_404_NOT_FOUND
                    )
    


    @swagger_auto_schema(
        method="put",
        operation_description="Обновление профиля партнера",
        operation_summary="Обновление профиля партнера",
        operation_id="update_partner_profile",
        tags=["Партнер"],
        responses={
            200: openapi.Response(description="OK - Профиль партнера успешно обновлен"),
            201: openapi.Response(description="Created - Профиль партнера успешно обновлен"),
            400: openapi.Response(description="Bad Request - Неверный запрос или некорректные данные"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            403: openapi.Response(description="Forbidden - Доступ запрещен"),
            404: openapi.Response(description="Not Found - Партнер не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user.id != request.user.id:
            return Response(
                {
                    'message': 'You are not allowed to update this profile.'
                    }, 
                status=403
            )
        user_data = request.data.pop('user', {})  # Извлечение данных пользователя из запроса
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Update user object if email is provided
        if user_data.get('email'):
            custom_user = instance.user
            custom_user.email = user_data['email']
            custom_user.save()

        return Response(serializer.data)
    
    



class ChatMessageCreateAPIView(APIView):
    @swagger_auto_schema(
        method="post",
        operation_description="Отправить сообщение",
        operation_summary="Создание нового сообщения",
        operation_id="send_message",
        tags=["Chat"],
        responses={
            201: openapi.Response(description="Created - Сообщение успешно отправлено"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=False, methods=["post"])
    def post(self, request, *args, **kwargs):
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            # Извлекаем текст сообщения и адрес получателя из сериализатора
            text = serializer.validated_data.get('text')
            recipient_email = serializer.validated_data.get('recipient_email')
            
            # Найдем получателя по адресу электронной почты
            recipient = CustomUser.objects.filter(email=recipient_email).first()
            if recipient:
                # Создаем новое сообщение
                chat_message = ChatMessage.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    text=text
                )
                return Response({'message': 'Сообщение успешно отправлено'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Получатель с указанным адресом электронной почты не найден'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    '''
    @action(detail=False, methods=["post"])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        return ChatMessage.objects.filter(recipient=user)'''







# class ChatMessageViewSet(viewsets.ModelViewSet):
#     queryset = ChatMessage.objects.all()
#     serializer_class = ChatMessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(sender=self.request.user)

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         user = self.request.user
#         # Фильтрация сообщений для текущего пользователя (отправленных или полученных)
#         queryset = queryset.filter(sender=user) | queryset.filter(recipient=user)
#         return queryset










    
    
    
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

    
    

{
    "name": "user0",
    "date_of_birth": "2000-01-01",
    "subscription": true
}


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


create establishment 
{
    "name": "dordoi",
    "location": "bishkek",
    "description": "trade center",
    "phone_number": 1234,
    "partner": 2
}

    
вот мой код 

модель 

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('partner', 'Partner'),
        ('regularuser', 'RegularUser'),)
    email = models.EmailField(unique=True, max_length=60, verbose_name="Email")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
class RegularUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    subscription = models.BooleanField(default=False, verbose_name="Subscription")
class Partner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    establishment_name = models.CharField(max_length=100, verbose_name="Establishment Name")
    location = models.CharField(max_length=100, verbose_name="Location")
    description = models.TextField(verbose_name="Description")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")


модель заведения

from django.db import models
from ..accounts.models import Partner

class Establishment(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    location = models.CharField(max_length=100, verbose_name="Location")
    description = models.TextField(verbose_name="Description")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Partner", related_name='establishments')

    class Meta:
        verbose_name = "Establishment"
        verbose_name_plural = "Establishments"

    def __str__(self):
        return self.name

вот представление 
class EstablishmentModelViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, method=["get"])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

вот сериализатор
from rest_framework import serializers
from apps.establishment.models import Establishment



class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = (
            'name',
            'description',
            'phone_number',
            'avatar',
            'partner'
        )


        
path("establishment/", EstablishmentModelViewSet.as_view({"get": "list"}), name="establishment-list"),
показывает пустой лист хотя есть заведения 

{
    "user_id": 2,
    "user": {
        "id": 2,
        "email": "partner_dordoi@mail.ru",
        "role": "partner"
    },
    "establishment_name": "dordoi market",
    "location": "bishkek",
    "description": "bazar",
    "phone_number": "12345"
}
    
    '''