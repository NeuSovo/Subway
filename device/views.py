# -*- coding: utf-8 -*-

from django.contrib import messages
from datetime import datetime

import django_excel as excel
from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError, transaction
from django.shortcuts import (HttpResponse, HttpResponseRedirect, get_object_or_404, render)
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView)

from core.utils import compress_file
from urllib.parse import quote
from .forms import DeviceForm, DeviceTestInfoForm, ProfessForm
from .models import *


class DeviceAddView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_create_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '%(name)s 添加成功'

    def post(self, request, **args):
        self.success_url = request.META.get('HTTP_REFERER') or self.success_url
        return super().post(request, *args)


class DeviceTestInfoUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Device
    form_class = DeviceTestInfoForm
    template_name = 'device/device_test_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '更新成功'

    def post(self, request, **args):
        self.success_url = request.META.get('HTTP_REFERER') or self.success_url
        return super().post(request, *args)


class DeviceUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_update_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '%(name)s 更新成功'

    def post(self, request, **args):
        self.success_url = request.META.get('HTTP_REFERER') or self.success_url
        return super().post(request, *args)

    def form_valid(self, form, **args):
        self.object.gen_qrcode_img()
        return super().form_valid(form, **args)


class DeviceDetailView(DetailView):
    model = Device
    template_name = "device/device_mobile.html"


class DeviceDeleteView(DeleteAjaxMixin, DeleteView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_delete_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '删除成功'

    def post(self, request, **args):
        self.success_url = request.META.get('HTTP_REFERER') or self.success_url
        return super().post(request, *args)


class DeviceListView(ListView):
    model = Device
    template_name = 'device/device.html'
    paginate_by = 50

    def __init__(self):
        super().__init__()
        self.profess_all = Profess.objects.all()
        self.profess = self.profess_all[0] if len(self.profess_all) > 0 else 0

    def get(self, request, *args, **kwargs):
        if not self.profess:
            return HttpResponseRedirect(reverse_lazy('device:init_profess'))
        profess_id = kwargs.get('profess_id')
        if profess_id:
            self.profess = get_object_or_404(Profess, pk=profess_id)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(DeviceListView, self).get_queryset()
        queryset = queryset.filter(profess=self.profess)
        print(len(queryset))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profess_s'] = self.profess_all
        context['select_profess'] = self.profess
        return context


class DeviceListDetailView(DeviceListView):
    template_name = 'device/device_list_detail.html'
    pass


class ProfessCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "device/add_update_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('device:list')


class ProfessInitView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "device/init_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('device:list')


class ProfessUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Profess
    form_class = ProfessForm
    template_name = "device/add_update_profess_form.html"
    success_message = '%(name)s 更新成功'
    success_url = reverse_lazy('device:list')

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
    template_name = "device/delete_profess.html"
    success_url = reverse_lazy('device:list')


def QR1(request):
    profess_s = Profess.objects.all()
    context = {'profess_s': profess_s, 'title': '设备信息', 'url': '/device/qr2/'

               }
    return render(request, 'system/profess_mobile.html', context=context)


def QR2(request, profess_id):
    profess = get_object_or_404(Profess, pk=profess_id)

    queryset = Device.objects.filter(profess=profess)
    context = {'object_list': queryset, 'select_profess': profess, 'title': '设备信息', 'url': '/device/detail/'}
    return render(request, 'system/professs_mobile.html', context=context)


def qr1_make(request):
    img = make_pic(['设备信息'], '/device/qr1')
    img.save('test.png')
    try:
        with open('test.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except Exception as e:
        raise e


def export_qr(request, dept_id=None):
    file_name = '设备二维码_'
    qr = Device.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d") + '.zip'
    s = compress_file([os.path.join(QR_DIR_3, QR_3_NAME_TEM % i.id) for i in qr])
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename={}".format(quote(file_name))
    s.seek(0)
    response.write(s.read())
    return response


def import_device_data(request):
    # 导入数据
    mapdict = {'名称': 'name', '设备状态': 'status_id', '专业id': 'profess_id', '验收人': 'acceptor', '站点': 'z1', '安装位置': 'z2',
               '主要部件生产厂家': 'z3', '材料名称': 'z4', '规格型号': 'z5', '进场时间': 'z6', '生产厂家': 'z7', '合格证号': 'z8', '使用部位': 'z9',
               '实验方式': 't1', '取样地点': 't2', '取样时间': 't3', '取样人': 't4', '检验项目': 't5', '检验日期': 't6', '执行标准': 't7',
               '保养内容': 't8', '注意事项': 't9', '现场验收结论': 't10', }
    if request.method == "POST":
        try:
            request.FILES['docfile'].save_to_database(name_columns_by_row=0, model=Device, mapdict=mapdict,
                                                      ignore_cols_at_names=['设备编号', '设备状态名字', '专业名称'])
            messages.success(request, "导入成功")

        except IntegrityError as e:
            print(e)
            messages.error(request, '导入失败：请检查Excel内容是否有以下错误: </br> 1.数据重复</br> 2.专业id不存在')
        except ValueError as e:
            print(e)
            messages.error(request, '导入失败：请检查Excel内容是否有以下错误: </br> 1.数据格式错误 例如id类存在汉字或字母')
        except Exception as e:
            messages.error(request, str(e))
        return JsonResponse({'msg': 'd'})
    else:
        pass


def export_device_data(request):
    file_name = '设备表_'
    queryset = Device.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d")

    column_names = ['id', 'name', 'status_id', 'status_name', 'profess_id', 'profess_name', 'acceptor', 'z1', 'z2',
                    'z3', 'z4', 'z5', 'z6', 'z7', 'z8', 'z9', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9',
                    't10']
    colnames = ['设备编号', '名称', '设备状态', '设备状态名字', '专业id', '专业名称', '验收人', '站点', '安装位置', '主要部件生产厂家', '材料名称', '规格型号', '进场时间',
                '生产厂家', '合格证号', '使用部位', '实验方式', '取样地点', '取样时间', '取样人', '检验项目', '检验日期', '执行标准', '保养内容', '注意事项', '现场验收结论']
    return excel.make_response_from_query_sets(queryset, column_names, 'xls', file_name=file_name, colnames=colnames,
                                               sheet_name='设备数据', ignore_rows=[0] if len(queryset) else [1])
