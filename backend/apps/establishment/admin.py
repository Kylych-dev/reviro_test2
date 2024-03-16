from django.contrib import admin
from .models import Establishment

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'locations', 'opening_hours', 'requirements')
    search_fields = ('name',)
    list_filter = ('locations',)