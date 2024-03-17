from django.db import models
from ..establishment.models import Establishment

class Beverage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    category = models.CharField(max_length=100, verbose_name="Category")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    description = models.TextField(verbose_name="Description")
    availability_status = models.BooleanField(default=True, verbose_name="Availability Status")
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, verbose_name="Establishment", related_name='beverages')

    class Meta:
        verbose_name = "Beverage"
        verbose_name_plural = "Beverages"

    def __str__(self):
        return self.name
