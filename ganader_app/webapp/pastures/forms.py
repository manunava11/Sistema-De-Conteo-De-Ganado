from django import forms
from .models import Pasture
from lots.models import Lot

class PastureForm(forms.ModelForm):
    class Meta:
        model = Pasture
        fields = ['name', 'area']

class LotSelectionForm(forms.Form):
    #lot_id = forms.ModelChoiceField(queryset=Lot.objects.filter(pasture__isnull=True), label="Available Lots")
    #lot_id = forms.ModelChoiceField(queryset=Lot.objects.all(), to_field_name='id', label='Select Lot')
    #lot_id = forms.ModelChoiceField(queryset=Lot.objects.filter(pasture__isnull=True), to_field_name='id', label='Select Lot')
    lot_id = forms.ModelChoiceField(
        queryset=Lot.objects.filter(pasture__isnull=True),
        to_field_name='id',
        label='Select Lot'
    )