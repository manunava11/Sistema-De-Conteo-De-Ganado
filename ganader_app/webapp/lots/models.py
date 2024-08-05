from django.db import models
from django.contrib.auth.models import User
from ranch.models import Ranch
from pastures.models import Pasture

class Lot(models.Model):
    CATEGORY_CHOICES = [
        ('terneros', 'Terneros'),
        ('terneras', 'Terneras'),
        ('novillos', 'Novillos'),
        ('vacas_de_invernada', 'Vacas de Invernada'),
        ('vaquillonas', 'Vaquillonas'),
        ('toros', 'Toros'),
    ]

    name = models.CharField(max_length=100)
    livestock_category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='terneros',
    )
    ranch = models.ForeignKey(Ranch, on_delete=models.CASCADE)
    pasture = models.ForeignKey(Pasture, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
