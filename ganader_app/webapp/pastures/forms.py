from django import forms
from .models import Pasture

class PastureForm(forms.ModelForm):
    class Meta:
        model = Pasture
        fields = ['name', 'area']