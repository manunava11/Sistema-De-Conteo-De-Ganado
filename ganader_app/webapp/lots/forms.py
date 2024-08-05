from django import forms
from .models import Lot
from cattle_countings.models import CowCount
from django.utils import timezone


class LotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = ['name', 'livestock_category']

class CowCountForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now
    )
    class Meta:
        model = CowCount
        fields = ['cow_count','date', 'comment']  # Add other fields as needed