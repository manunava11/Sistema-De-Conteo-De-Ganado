from django import forms
from .models import CowCount
from django.utils import timezone

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = CowCount
        fields = []

class ManualCountForm(forms.ModelForm):
    class Meta:
        date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now
        )
        model = CowCount
        fields = ['cow_count','date', 'comment']