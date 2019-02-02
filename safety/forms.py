from django import forms
from .models import SafetyFile


class SafetyFileForm(forms.ModelForm):
    class Meta:
        model = SafetyFile
        fields = '__all__'
