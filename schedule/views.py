# -*- coding: utf-8 -*-  

from django.contrib import messages
from datetime import datetime

import django_excel as excel
from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, render)
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from core.QR import make_pic
from core.utils import compress_file
from urllib.parse import quote
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

    def post(self, request, **args):
        self.success_url = request.META.get('HTTP_REFERER') or self.success_url
        return super().post(request, *args)

    def form_valid(self, form, **args):
        self.object.gen_qrcode_img()
        return super().form_valid(form, **args)


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

    def post(self, request, **args):
        self.success_url = request.META.get('HTTP_REFERER') or self.success_url
        return super().post(request, *args)

    def form_valid(self, form, **args):
        self.object.gen_qrcode_img()
        return super().form_valid(form, **args)


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
    img = make_pic(['进度信息'], '/schedule/qr1')
    img.save('test.png')
    try:
        with open('test.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except Exception as e:
        raise e


def qr4_make(request):
    img = make_pic(['进度总图表'], '/schedule/mobile')
    img.save('test.png')
    try:
        with open('test.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except Exception as e:
        raise e


def export_qr(request, dept_id=None):
    file_name = '进度二维码_'
    qr = Schedule.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d") + '.zip'
    s = compress_file(
        [os.path.join(QR_DIR_3, QR_3_NAME_TEM % i.id) for i in qr])
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename={}".format(quote(file_name))
    s.seek(0)
    response.write(s.read())
    return response


def import_schedule_data(request):
    # 导入数据
    mapdict = {
        '作业名称': 'job_name',
        '专业id': 'profess_id',
        '单位': 'unit',
        '施工地点': 'location',
        '开累完成量': 'done_count',
        '设计总量': 'design_total',
        '上周计划完成量': 'last_week_plan',
        '上周实际完成量': 'last_week_actual',
        '本周计划完成量': 'now_week_plan',
        '完成总周数': 'now_week_actual',
        '当前周目': 'now_week',
    }
    if request.method == "POST":
        try:
            request.FILES['docfile'].save_to_database(
                name_columns_by_row=0,
                model=Schedule,
                mapdict=mapdict,
                ignore_cols_at_names=['进度编号', '专业名称'])
            messages.success(request, "导入成功")

        except IntegrityError as e:
            print(e)
            messages.error(
                request, '导入失败：请检查Excel内容是否有以下错误: </br> 1.数据重复</br> 2.专业id不存在')
        except ValueError as e:
            print(e)
            messages.error(
                request, '导入失败：请检查Excel内容是否有以下错误: </br> 1.数据格式错误 例如id类存在汉字或字母')
        except Exception as e:
            messages.error(request, str(e))
        return JsonResponse({'msg': 'd'})
    else:
        pass


def export_schedule_data(request):
    file_name = '进度表_'
    queryset = Schedule.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d")

    column_names = ['id', 'job_name', 'profess_id', 'profess_name', 'unit', 'location', 'done_count', 'design_total',
                    'last_week_plan', 'last_week_actual', 'now_week_plan', 'now_week_actual', 'now_week']
    colnames = ['进度编号', '作业名称', '专业id', '专业名称', '单位',
                '施工地点', '开累完成量', '设计总量', '上周计划完成量', '上周实际完成量', '本周计划完成量', '完成总周数', '当前周目']
    return excel.make_response_from_query_sets(
        queryset,
        column_names,
        'xls',
        file_name=file_name,
        colnames=colnames,
        sheet_name='进度数据',
        ignore_rows=[0] if len(queryset) else [1]
    )
