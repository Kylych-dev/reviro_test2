from rest_framework import serializers, permissions
from django.utils import timezone
from datetime import datetime, timedelta


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить чтение всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить запись только владельцу объекта
        return obj.user == request.user


class IsPartnerOrReadOnly(permissions.BasePermission):
    '''
    Разрешает чтение всем пользователям,
    но позволяет обновление, создание и 
    удаление только партнерам.
    '''

    def has_permission(self, request, view):
        # Разрешить чтение всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Для остальных методов проверяем, является ли пользователь партнером
        return request.user and request.user.role == 'partner'    


def unique_order_per_establishment_validator(value):
    '''
    только один заказ в одном месте в течение дня
    '''
    user = value.user
    establishment = value.establishment
    today = datetime.now().date()
    if user.order_set.filter(establishment=establishment, created_at__date=today).exists():
        raise serializers.ValidationError(
            "Вы уже разместили заказ в этом заведении сегодня."
            )


class CustomPermission(permissions.BasePermission):
    '''
    разместить только один заказ в течение часа.
    '''
    def has_permission(self, request, view):
        user = request.user
        last_order_time = user.order_set.last().created_at
        if last_order_time:
            time_since_last_order = timezone.now() - last_order_time
            if time_since_last_order < timedelta(hours=1):
                return False
        return True
