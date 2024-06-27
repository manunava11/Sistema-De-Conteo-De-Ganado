from django.db import models
from django.conf import settings
from ranch.models import Ranch  # Adjust the import path according to your project structure

class Pasture(models.Model):
    name = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=10, decimal_places=2)  # Example field
    ranch = models.ForeignKey(Ranch, related_name='ranch', on_delete=models.CASCADE)

    def __str__(self):
        return self.name