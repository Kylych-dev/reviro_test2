from rest_framework import serializers
from api.utils.permissions import unique_order_per_establishment_validator
from apps.order.models import Order



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'user',
            'establishment',
            'beverage',
            'order_date'
        )
        validators = [                                  # только один заказ в одном месте в течение дня
            unique_order_per_establishment_validator
        ]


'''
    user
    establishment
    beverage
    order_date 
'''