from django import forms
from .models import Pasture
from lots.models import Lot

class PastureForm(forms.ModelForm):
    class Meta:
        model = Pasture
        fields = ['name', 'area']

class LotSelectionForm(forms.Form):
    lot_id = forms.ModelChoiceField(
        queryset=Lot.objects.all(),
        label='Select Lot',
        required=False,
        empty_label='No Lot'  # Add an empty option
    )