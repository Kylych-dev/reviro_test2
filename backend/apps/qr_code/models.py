from django.db import models

from apps.accounts.models import Partner
from apps.beverage.models import Beverage



class QRCode(models.Model):
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, verbose_name="Partner")
    qr_code_image = models.ImageField(upload_to='qr_codes', verbose_name="QR Code Image")
    beverage_menu = models.ManyToManyField(Beverage, verbose_name="Beverage Menu")

    class Meta:
        verbose_name = "QR Code"
        verbose_name_plural = "QR Codes"

    def __str__(self):
        return f"QR Code for {self.partner.establishment_name}"
    
