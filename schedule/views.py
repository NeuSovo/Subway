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
from core.QR import make_pic


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
    template_name = "schedule/schedule_mobile.html"


class ScheduleDeleteView(DeleteAjaxMixin, DeleteView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_delete_form.html'
    success_url = reverse_lazy('schedule:list')
    success_message = '删除成功'


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


class ScheduleListMobileView(ScheduleListView):
    model = Schedule
    template_name = "schedule/schedule_chart_mobile.html"


class ScheduleItemMobileView(DetailView):
    model = Schedule
    template_name = "schedule/schedule_item_mobile.html"


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


def QR1(request):
    profess_s = Profess.objects.all()
    context = {
        'profess_s': profess_s,
        'title': '进度信息',
        'url': '/schedule/qr2/'

    }
    return render(request, 'system/profess_mobile.html', context=context)


def QR2(request, profess_id):
    profess = get_object_or_404(Profess, pk=profess_id)

    queryset = Schedule.objects.filter(profess=profess)
    context = {
        'object_list': queryset,
        'select_profess': profess,
        'title': '进度信息',
        'url': '/schedule/detail/'
    }
    return render(request, 'system/professs_mobile.html', context=context)


def qr1_make(request):
    img = make_pic(['进度信息', '全部专业'], '/schedule/qr1')
    img.save('test.png')
    try:
        with open('test.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except Exception as e:
        raise e


def qr4_make(request):
    img = make_pic(['进度总图表', '全部专业'], '/schedule/mobile')
    img.save('test.png')
    try:
        with open('test.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except Exception as e:
        raise e
