from rest_framework import serializers
from apps.accounts.models import RegularUser, CustomUser, Partner



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 
            'email', 
            'role'
            ]
        read_only_fields = [
            'id'
            ]


class RegularUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)  # поле для идентификатора пользователя

    class Meta:
        model = RegularUser
        fields = [
            'user_id', 
            'user', 
            'name', 
            'date_of_birth', 
            'subscription'
            ]


class PartnerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)  # поле для идентификатора пользователя

    class Meta:
        model = Partner
        fields = [
            'user_id', 
            'user', 
            'establishment_name', 
            'location', 
            'description', 
            'phone_number'
            ]















'''
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





'''



'''

class RegularUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        fields = [
            'user', 
            'name', 
            'date_of_birth', 
            'avatar'
            ]
'''