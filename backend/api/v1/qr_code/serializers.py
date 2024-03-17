from rest_framework import serializers
from apps.qr_code.models import QRCode



class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = (
            'partner',
            'qr_code_image',
            'beverage_menu',
        )




'''
partner
qr_code_image
beverage_menu
'''