from rest_framework import serializers
from apps.beverage.models import Beverage



class BeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beverage
        fields = (
            'name',
            'category',
            'price',
            'description',
            'availability_status',
            'establishment'
        )



'''
name
category
price
description
availability_status
establishment
'''

