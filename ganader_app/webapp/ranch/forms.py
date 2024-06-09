from django import forms
from django.contrib.auth.models import User
from .models import Ranch

class RanchForm(forms.ModelForm):
    class Meta:
        model = Ranch
        fields = ['name', 'description']

class AddMemberForm(forms.Form):
    username = forms.CharField(max_length=150)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f"User '{username}' does not exist.")
        return username