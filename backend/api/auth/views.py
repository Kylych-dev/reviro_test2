from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import update_session_auth_hash
from datetime import datetime


from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django_rest_passwordreset.models import ResetPasswordToken


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
    ChangePasswordSerializer,
    ResetPasswordEmailSerializer
    )


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
        if request.method == 'POST':
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get('old_password')):
                    user.set_password(serializer.data.get('new_password'))
                    user.save()
                    update_session_auth_hash(request, user)  # Обновляем сессию после изменения пароля
                    return Response(
                        {'message': 'Password changed successfully.'}, 
                        status=status.HTTP_200_OK
                        )
                return Response(
                    {'error': 'Incorrect old password.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )

'''
    def post(self, request):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            UserModel = CustomUser
            try:
                user = UserModel.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response(
                    {'error': 'Пользователь с таким email не найден.'}, 
                    status=status.HTTP_404_NOT_FOUND
                    )
            
            # Создание токена сброса пароля
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_str(user.pk).encode())
            ResetPasswordToken.objects.update_or_create(user=user, defaults={'key': token})
            
            # Отправка электронного письма с инструкциями по сбросу пароля
            reset_password_url = f"{request.build_absolute_uri('/reset-password-confirm/')}?uid={uid}&token={token}"
            # Здесь добавьте код для отправки электронного письма с reset_password_url
            
            return Response({'message': 'Email with reset password instructions has been sent.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
    
    



























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



































'''

class RegisterView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    def register(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                validated_data = serializer.validated_data
                # validated_data.pop("password2")
                user = CustomUser(
                    **validated_data,
                )
                user.set_password(validated_data.get("password"))
                user.save()
                return Response(
                    serializer.data, 
                    status=status.HTTP_201_CREATED
                    )

            except Exception as ex:
                return Response(
                    data={"error": f"User creation failed: {str(ex)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )


class UserAuthenticationView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def login(self, request):
        print(request.data, '/*/*/*/*/*/*')
        phone_number = request.data["email"]
        password = request.data["password"]

        try:
            # phone_number = normalize_phone_number(phone_number)
            # user = CustomUser.objects.get(phone_number=phone_number)
            user = CustomUser.objects.get(email=phone_number)


        except CustomUser.DoesNotExist:
            print('hello')
            raise AuthenticationFailed("Такого пользователя не существует")

        if user is None:
            raise AuthenticationFailed("Такого пользователя не существует")

        # if not user.check_password(password):
        #     raise AuthenticationFailed("Не правильный пароль")

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        print('ok')
        return Response(
            data={
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            },
            status=status.HTTP_200_OK,
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
        

        '''