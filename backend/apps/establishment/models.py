from django.db import models
import uuid

class Establishment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    locations = models.CharField(max_length=255, verbose_name="Locations")
    opening_hours = models.CharField(max_length=100, verbose_name="Opening Hours")
    requirements = models.TextField(verbose_name="Requirements")

    class Meta:
        verbose_name = "Establishment"
        verbose_name_plural = "Establishments"

    def __str__(self):
        return self.name
    
    