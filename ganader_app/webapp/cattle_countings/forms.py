from django import forms
from .models import VideoUpload, CountHistory

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['lot', 'video']

class ManualCountForm(forms.ModelForm):
    class Meta:
        model = CountHistory
        fields = ['lot', 'cow_count']