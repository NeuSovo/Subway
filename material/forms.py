from django import forms
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Material, Profess


class MaterialForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'


class ProfessForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):


    """Form definition for Profess."""

    class Meta:
        """Meta definition for Professform."""

        model = Profess
        fields = '__all__'