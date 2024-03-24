from rest_framework.decorators import action
from rest_framework import views, status, permissions
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView


from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.accounts.models import (
    RegularUser, 
    Partner, 
    CustomUser,
    ChatMessage
    )
from .serializers import (
    RegularUserSerializer, 
    PartnerSerializer, 
    ChatMessageSerializer,
    )


class RegularUserUpdateView(generics.UpdateAPIView):
    queryset = RegularUser.objects.all()
    serializer_class = RegularUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        regular_user_id = self.kwargs.get('pk')
        try:
            return RegularUser.objects.get(pk=regular_user_id)
        except RegularUser.DoesNotExist:
            return Response(
                {'message': 'RegularUser not found'}, 
                status=status.HTTP_404_NOT_FOUND
                )
    

    @swagger_auto_schema(
        operation_description="Обновление профиля обычного пользователя",
        operation_summary="Обновление профиля обычного пользователя",
        operation_id="update_++++user_profile",
        tags=["User"],
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


        # if instance.user.id != request.user.id:
        if not isinstance(instance, RegularUser):
            return Response(
                {'message': 'RegularUser not found'}, 
                status=status.HTTP_404_NOT_FOUND
                )

        if instance.user.id != request.user.id:
            return Response(
                {
                    'message': 'You are not allowed to update this profile.'
                    }, 
                status=status.HTTP_403_FORBIDDEN
                )
        
        user_data = request.data.pop('user', {})  # Извлечение данных пользователя из запроса
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if user_data.get('email'):
            custom_user = instance.user
            custom_user.email = user_data['email']
            custom_user.save()

        return Response(serializer.data)
    

    
class PartnerUpdateView(generics.UpdateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [permissions.IsAuthenticated,]

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
        operation_description="Обновление профиля партнера",
        operation_summary="Обновление профиля партнера",
        operation_id="update_partner",
        tags=["User-update"],
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

        if not isinstance(instance, Partner):
            return Response(
                {'message': 'RegularUser not found'}, 
                status=status.HTTP_404_NOT_FOUND
                )
        
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

        if user_data.get('email'):
            custom_user = instance.user
            custom_user.email = user_data['email']
            custom_user.save()

        return Response(serializer.data)
    

class ChatMessageCreateAPIView(APIView):
    @swagger_auto_schema(
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
                return Response(
                    {'message': 'Сообщение успешно отправлено'}, 
                    status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    {'error': 'Получатель с указанным адресом электронной почты не найден'}, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        if email:
            user = CustomUser.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"https://yourwebsite.com/reset-password/{uid}/{token}/"
                subject = 'Password Reset'
                message = render_to_string('email/password_reset_email.html', {
                    'reset_link': reset_link,
                })
                send_mail(subject, message, 'tteest624@gmail.com', [email])
                return Response({'detail': 'Password reset link has been sent'}, status=status.HTTP_200_OK)
        return Response({'detail': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)


        
    
    
'''   
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

'''