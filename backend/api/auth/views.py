from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from datetime import datetime

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.accounts.models import (
    CustomUser, 
    Partner, 
    RegularUser
    )

from .serializers import (
    CustomUserSerializer, 
    PartnerSerializer, 
    RegularUserSerializer,
    )


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация пользователя.",
        operation_summary="Регистрация пользователя",
        operation_id="register_user",
        tags=["Authentication"],
        responses={
            200: openapi.Response(description="OK - Пользователь зарегистрирован."),
            201: openapi.Response(description="Created - Пользователь успешно создан."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )


class RegularUserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация пользователя.",
        operation_summary="Регистрация пользователя",
        operation_id="register_regular_user",
        tags=["Authentication"],
        responses={
            201: openapi.Response(description="Created - пользователь успешно создан."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def post(self, request):
        serializer = RegularUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )


class PartnerRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация партнера.",
        operation_summary="Регистрация партнера",
        operation_id="register_partner",
        tags=["Authentication"],
        responses={
            201: openapi.Response(description="Created - Партнер успешно создан."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def post(self, request):
        serializer = PartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )


class UserAuthenticationView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Аутентификация пользователя.",
        operation_summary="Вход пользователя",
        operation_id="user_login",
        tags=["Authentication"],
        responses={
            200: openapi.Response(description="OK - Пользователь успешно аутентифицирован."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
            401: openapi.Response(description="Unauthorized - Не авторизован."),
        },
    )
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:                                                    # Провеорка в БД пользователя 
            custom_user = CustomUser.objects.get(email=email)
            regular_user = custom_user.role
        except RegularUser.DoesNotExist:
            raise AuthenticationFailed("Такого пользователя не существует")

        if custom_user is None or regular_user is None:
            raise AuthenticationFailed("Такого пользователя не существует")

        if not custom_user.check_password(password):
            raise AuthenticationFailed("Не правильный пароль")

        access_token = AccessToken.for_user(custom_user)
        refresh_token = RefreshToken.for_user(custom_user)

        # ___________________________________________________________
        # Допольнительная ифнормация о токене
        access_token_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
        refresh_token_lifetime = api_settings.REFRESH_TOKEN_LIFETIME
        current_datetime = datetime.now()
        access_token_expiration = current_datetime + access_token_lifetime
        refresh_token_expiration = current_datetime + refresh_token_lifetime
        # ___________________________________________________________

        return Response(
            data={
                "access_token": str(access_token),
                "access_token_expires": access_token_expiration.strftime("%Y-%m-%d %H:%M:%S"),

                "refresh_token": str(refresh_token),
                "refresh_token_expires": refresh_token_expiration.strftime("%Y-%m-%d %H:%M:%S"),
                
                "token_type": "access",
                "status": "success"
            },
            status=status.HTTP_200_OK,
        )
    
    @swagger_auto_schema(
        operation_description="Выход пользователя.",
        operation_summary="Выход пользователя",
        operation_id="user_logout",
        tags=["Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(description="OK - Пользователь успешно вышел из учетной записи."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def logout(self, request):
        try:
            if "refresh_token" in request.data:
                refresh_token = request.data["refresh_token"]
                if refresh_token:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                return Response("Вы вышли из учетной записи", status=status.HTTP_200_OK)
            else:
                return Response(
                    "Отсутствует refresh_token", status=status.HTTP_400_BAD_REQUEST
                )
        except TokenError:
            raise AuthenticationFailed("Не правильный токен")



class ChangePasswordAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema(
        operation_description="Изменить пароль",
        operation_summary="Смена пароля пользователя",
        operation_id="change_password",
        tags=["Authentication"],
        responses={
            200: openapi.Response(description="OK - Пароль успешно изменен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
        },
    )
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
                send_mail(subject, message, 'from@example.com', [email])
                return Response({'detail': 'Password reset link has been sent'}, status=status.HTTP_200_OK)
        return Response({'detail': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)






'''
register partner

{
    "user": {
        "email": "user@mail.ru",
        "role": "partner",
        "password": 1
    },
    "establishment_name": "ramstor",
    "location": "bishkek",
    "description": "trade center",
    "phone_number": 12345
}
'''