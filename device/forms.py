from django import forms
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Device, Profess


class DeviceForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'


class ProfessForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):


    """Form definition for Profess."""

    class Meta:
        """Meta definition for Professform."""

        model = Profess
        fields = '__all__'