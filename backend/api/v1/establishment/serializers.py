from rest_framework import serializers
from apps.establishment.models import Establishment



class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = (
            'name',
            'description',
            'locations',
            'opening_hours',
            'requirements'
        )



'''
    id 
    name 
    description
    locations 
    opening_hours
    requirements

'''