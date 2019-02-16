from django import forms
from .models import TechnologyFile, Profess
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class TechnologyFileForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):


    """Form definition for TechnologyFile."""

    class Meta:
        """Meta definition for TechnologyFileform."""

        model = TechnologyFile
        fields = '__all__'


class ProfessForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):


    """Form definition for Profess."""

    class Meta:
        """Meta definition for Professform."""

        model = Profess
        fields = '__all__'