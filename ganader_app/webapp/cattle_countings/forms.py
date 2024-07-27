from django import forms
from .models import CowCount, UploadedVideo
from django.utils import timezone

class VideoUploadForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    comment = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = UploadedVideo
        fields = ['uploaded_video', 'date', 'comment']

class ManualCountForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    class Meta:
        model = CowCount
        fields = ['cow_count', 'date', 'comment']