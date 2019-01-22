from django import forms
from .models import TechnologyFile

class TechnologyFileForm(forms.ModelForm):
    """Form definition for TechnologyFile."""

    class Meta:
        """Meta definition for TechnologyFileform."""

        model = TechnologyFile
        fields = '__all__'
