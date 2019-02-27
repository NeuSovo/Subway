from django import forms
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Schedule, Profess


class ScheduleForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'


class ProfessForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:

        model = Profess
        fields = '__all__'
