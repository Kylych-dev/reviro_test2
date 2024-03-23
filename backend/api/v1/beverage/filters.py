from django_filters import rest_framework as filters
from apps.beverage.models import Beverage

class BeverageFilter(filters.FilterSet):
    available = filters.BooleanFilter(field_name='availability_status')

    class Meta:
        model = Beverage
        fields = ['availability_status']