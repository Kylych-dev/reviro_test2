from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(
    #     write_only=True, required=True, validators=[validate_password]
    # )
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(required=True)


    class Meta:
        model = CustomUser
        fields = (
            "password",
            "email",
        )
        # extra_kwargs = {
        #     "password": {"write_only": True},
        #     "first_name": {"required": True},
        #     "last_name": {"required": True},
        # }
