from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.response import Response

from apps.accounts.models import (
    CustomUser, 
    Partner, 
    RegularUser
    )

from .serializers import (
    CustomUserSerializer, 
    PartnerSerializer, 
    RegularUserSerializer
    )


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
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






class RegularUserAuthenticationView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    def login(self, request):
        print(request, '*****************')
        print('\n')
        print(request.data, '*****************')

        email = request.data.get('email')
        password = request.data.get('password')

        try:
            custom_user = CustomUser.objects.get(email=email)
            regular_user = custom_user.regularuser
            print(custom_user.role, '<<<<<<<-------------------------')
        except RegularUser.DoesNotExist:
            raise AuthenticationFailed("Такого пользователя не существует")

        if custom_user is None or regular_user is None:
            raise AuthenticationFailed("Такого пользователя не существует")

        if not custom_user.check_password(password):
            raise AuthenticationFailed("Не правильный пароль")

        access_token = AccessToken.for_user(custom_user)
        refresh_token = RefreshToken.for_user(custom_user)

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