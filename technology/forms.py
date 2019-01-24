from django import forms
from .models import TechnologyFile
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class TechnologyFileForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    """Form definition for TechnologyFile."""

    class Meta:
        """Meta definition for TechnologyFileform."""

        model = TechnologyFile
        fields = '__all__'
