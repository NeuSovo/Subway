from django import forms
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.core.exceptions import ValidationError
from .models import *


class ScheduleForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

    def clean_done_count(self):
        design_total = self.data.get('design_total')
        value = self.data.get('done_count')
        if int(value) < 0:
            raise ValidationError("请确保该值大于或等于0")
        if int(value) > int(design_total):
            raise ValidationError("请确保该值不大于设计总量")
        return value


class ProfessForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:

        model = Profess
        fields = '__all__'
