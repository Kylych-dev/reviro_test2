from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.accounts.models import CustomUser
from .serializers import CustomUserSerializer
from core.utils import normalize_email


class RegisterView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        operation_description="Создание нового пользователя",
        operation_summary="Создание нового пользователя",
        operation_id="register_user",
        tags=["Authentication"],
        responses={
            201: openapi.Response(description="OK - Регистрация прошла успешно."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
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

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        operation_description="Авторизация пользователя для получения токена.",
        operation_summary="Авторизация пользователя для получения токена",
        operation_id="login_user",
        tags=["Authentication"],
        responses={
            200: openapi.Response(
                description="OK - Авторизация пользователя прошла успешно."
            ),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
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

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        operation_description="Выход для удаления токена.",
        operation_summary="Выход для удаления токена",
        operation_id="logout_user",
        tags=["Authentication"],
        responses={
            201: openapi.Response(
                description="OK - Выход пользователя прошла успешно."
            ),
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
        

        