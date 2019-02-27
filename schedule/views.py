from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, render)
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from .forms import *

class ScheduleAddView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_create_form.html'
    success_url = reverse_lazy('schedule:list')
    success_message = '%(job_name)s 添加成功'


class ScheduleUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_update_form.html'
    success_url = reverse_lazy('schedule:list')
    success_message = '%(job_name)s 更新成功'


class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = "TEMPLATE_NAME"


class ScheduleDeleteView(DeleteAjaxMixin, DeleteView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_delete_form.html'
    success_url = reverse_lazy('schedule:list')


class ScheduleListView(ListView):
    model = Schedule
    template_name = "schedule/schedule.html"
    paginate_by = 100

    def __init__(self):
        super().__init__()
        self.profess_all = Profess.objects.all()
        self.profess = self.profess_all[0] if len(self.profess_all) > 0 else 0

    def get(self, request, *args, **kwargs):
        if not self.profess:
            return HttpResponseRedirect(reverse_lazy('schedule:init_profess'))
        profess_id = kwargs.get('profess_id')
        if profess_id:
            self.profess = get_object_or_404(Profess, pk=profess_id)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(ScheduleListView, self).get_queryset()
        queryset = queryset.filter(profess=self.profess)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profess_s'] = self.profess_all
        context['select_profess'] = self.profess
        return context


class ScheduleListDetailView(ScheduleListView):
    model = Schedule
    template_name = "schedule/schedule_detail.html"


class ScheduleListChartView(ScheduleListView):
    model = Schedule
    template_name = "schedule/schedule_chart.html"


class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = "NAME"


class ScheduleItemChartView(DetailView):
    model = Schedule
    template_name = "schedule/schedule_item.html"


class ProfessCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "schedule/add_update_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('schedule:list')


class ProfessInitView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "schedule/init_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('schedule:list')


class ProfessUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Profess
    form_class = ProfessForm
    template_name = "schedule/add_update_profess_form.html"
    success_message = '%(name)s 更新成功'
    success_url = reverse_lazy('schedule:list')


class ProfessDeleteView(DeleteView):
    model = Profess
    form_class = ProfessForm
    success_message = '%(name)s 删除成功'
    template_name = "schedule/delete_profess.html"
    success_url = reverse_lazy('schedule:list')
