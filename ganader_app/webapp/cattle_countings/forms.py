from django import forms
from .models import CowCount

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = CowCount
        fields = []

class ManualCountForm(forms.ModelForm):
    class Meta:
        model = CowCount
        fields = ['cow_count','date', 'comment']