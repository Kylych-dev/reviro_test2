from rest_framework import serializers
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


'''
    user
    establishment
    beverage
    order_date 

'''