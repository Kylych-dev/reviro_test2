from rest_framework import serializers
from apps.establishment.models import Establishment



class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = '__all__'
        # fields = (
        #     'name',
        #     'description',
        #     'phone_number',
        #     'avatar',
        #     'partner'
        # )



'''
    name
    location
    description
    phone_number
    avatar
    partner
'''