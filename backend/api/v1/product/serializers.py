from rest_framework import serializers
from apps.product.models import Product



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ( 
            'id',
            'name',
            'description', 
            'price', 
            'quantity_in_stock' 
        )



'''

    id 
    name 
    description 
    price 
    quantity_in_stock 


'''