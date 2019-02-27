from django import forms
from .models import SafetyFile
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class SafetyFileForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = SafetyFile
        fields = '__all__'
