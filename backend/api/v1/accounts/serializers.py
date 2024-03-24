from rest_framework import serializers
from apps.accounts.models import (
    RegularUser, 
    CustomUser, 
    Partner, 
    ChatMessage
    )



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



class ChatMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    recipient_email = serializers.EmailField(required=True)

    class Meta:
        model = ChatMessage
        fields = [
            # 'sender_email', 
            'recipient_email', 
            'text', 
            'timestamp'
            ]

    def get_sender_email(self, obj):
        return obj.sender.email

    def get_recipient_email(self, obj):
        return obj.recipient.email









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