from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'quantity_in_stock')
    search_fields = ('name',)
    list_filter = ('price', 'quantity_in_stock')

    