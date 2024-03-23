from django.db import models
from ..accounts.models import Partner

class Establishment(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    location = models.CharField(max_length=100, verbose_name="Location")
    description = models.TextField(verbose_name="Description")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Partner", related_name='establishments')

    class Meta:
        verbose_name = "Establishment"
        verbose_name_plural = "Establishments"

    def __str__(self):
        return self.name
    




