from django import forms
from .models import Lot

class LotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = ['name', 'livestock_category', 'cow_count']