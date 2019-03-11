from django import forms
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Device, Profess


class DeviceForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Device
        fields = ('id', 'name', 'status_id', 'profess', 'file_s', 'z1', 'z2','z3','z4','z5','z6','z7','z8','z9')


class ProfessForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        """Meta definition for Professform."""

        model = Profess
        fields = '__all__'


class DeviceTestInfoForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Device
        fields = ('acceptor', 't1', 't2', 't3', 't4',
                  't5', 't6', 't7', 't8', 't9', 't10')
