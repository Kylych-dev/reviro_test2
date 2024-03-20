from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.accounts.models import (
    CustomUser, 
    Partner, 
    RegularUser
)



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class PartnerSerializer(serializers.ModelSerializer):
    # user = CustomUserSerializer(read_only=True)
    user = CustomUserSerializer()

    class Meta:
        model = Partner
        fields = '__all__'

    def create(self, validated_data):
        print('---->', validated_data)
        user_data = validated_data.pop('user')
        role = user_data.pop('role')
        user = CustomUser.objects.create_user(role=role, **user_data)
        student = Partner.objects.create(user=user, **validated_data)
        return student


class RegularUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = RegularUser
        fields = '__all__'

    def create(self, validated_data):
        print('---->', validated_data)
        user_data = validated_data.pop('user')
        role = user_data.pop('role')
        user = CustomUser.objects.create_user(role=role, **user_data)
        student = RegularUser.objects.create(user=user, **validated_data)
        return student

