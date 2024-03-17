from django.db import models
from apps.accounts.models import CustomUser
from apps.beverage.models import Beverage
from apps.establishment.models import Establishment


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="User")
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, verbose_name="Establishment", related_name='orders')
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE, verbose_name="Beverage")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Order Date")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"