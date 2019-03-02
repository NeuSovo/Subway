# -*- coding: utf-8 -*-  

from django.contrib import messages
from datetime import datetime

import django_excel as excel
from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError, transaction
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, render)
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from core.utils import compress_file

from .forms import DeviceForm, DeviceTestInfoForm, ProfessForm
from .models import *


class DeviceAddView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_create_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '%(name)s 添加成功'


class DeviceTestInfoUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = DeviceTestInfo
    form_class = DeviceTestInfoForm
    template_name = 'device/device_create_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '更新成功'


class DeviceUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_update_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '%(name)s 更新成功'


class DeviceDetailView(DetailView):
    model = Device
    template_name = "device/device_mobile.html"


class DeviceDeleteView(DeleteAjaxMixin, DeleteView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_delete_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '删除成功'


class DeviceListView(ListView):
    model = Device
    template_name = 'device/device.html'
    paginate_by = 100

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


class ProfessDeleteView(DeleteView):
    model = Profess
    form_class = ProfessForm
    success_message = '%(name)s 删除成功'
    template_name = "device/delete_profess.html"
    success_url = reverse_lazy('device:list')


def QR1(request):

    profess_s = Profess.objects.all()
    context = {
        'profess_s': profess_s,
        'title': '设备信息',
        'url': '/device/qr2/'

    }
    return render(request, 'system/profess_mobile.html', context=context)


def QR2(request, profess_id):
    profess = get_object_or_404(Profess, pk=profess_id)

    queryset = Device.objects.filter(profess=profess)
    context = {
        'object_list': queryset,
        'select_profess': profess,
        'title': '设备信息',
        'url': '/device/detail/'
    }
    return render(request, 'system/professs_mobile.html', context=context)


def qr1_make(request):
    img = make_pic(['设备信息', '全部专业'], '/device/qr1')
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
    s = compress_file(
        [os.path.join(QR_DIR_3, QR_3_NAME_TEM % i.id) for i in qr])
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=" + \
                                      file_name.encode(
                                          'utf-8').decode('ISO-8859-1')
    s.seek(0)
    response.write(s.read())
    return response


def import_device_data(request):
    # 导入数据
    mapdict = {
        '名称': 'name',
        '设备状态': 'status_id',
        '专业id': 'profess_id',
        '站点': 'z1',
        '安装位置': 'z2',
        '主要部件生产厂家': 'z3',
        '材料名称': 'z4',
        '规格型号': 'z5',
        '进场时间': 'z6',
        '生产厂家': 'z7',
        '合格证号': 'z8',
        '使用部位': 'z9',
    }
    if request.method == "POST":
        try:
            request.FILES['docfile'].save_to_database(
                name_columns_by_row=0,
                model=Device,
                mapdict=mapdict)
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


def export_device_data(request):
    file_name = '设备表_'
    queryset = Device.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d")

    column_names = ['id', 'name', 'status_id', 'status_name', 'profess_id', 'profess_name',
                    'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7', 'z8', 'z9']
    colnames = ['设备编号', '名称', '设备状态', '设备状态名字', '专业id', '专业名称',
                '站点', '安装位置', '主要部件生产厂家', '材料名称', '规格型号', '进场时间', '生产厂家', '合格证号', '使用部位']
    return excel.make_response_from_query_sets(
        queryset,
        column_names,
        'xls',
        file_name=file_name,
        colnames=colnames,
        sheet_name='设备数据',
    )


def export_device_test_data(request):
    file_name = '设备验收数据表_'
    queryset = DeviceTestInfo.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d")

    column_names = ['device_id', 'device_name',
                    'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7', 'z8', 'z9', 'z10', 'acceptor']
    colnames = ['设备编号', '名称', '实验方式', '取样地点', '取样时间', '取样人',
                '检验项目', '检验日期', '执行标准', '保养内容', '注意事项', '现场验收结论', '验收人']
    return excel.make_response_from_query_sets(
        queryset,
        column_names,
        'xls',
        file_name=file_name,
        colnames=colnames,
        sheet_name='设备验收数据',
    )


# def import_device_test_data(request):
#     # 导入数据
#     mapdict = {
#         '设备编号': 'device_id',
#         '实验方式': 'z1',
#         '取样地点': 'z2',
#         '取样时间': 'z3',
#         '取样人': 'z4',
#         '检验项目': 'z5',
#         '检验日期': 'z6',
#         '执行标准': 'z7',
#         '保养内容': 'z8',
#         '注意事项': 'z9',
#         '现场验收结论': 'z10',
#         '验收人': 'acceptor',
#     }

#     def ignore_row(row):
#         print (row[0])
#         return row
#     if request.method == "POST":
#         try:
#             request.FILES['docfile'].save_to_database(
#                 name_columns_by_row=0,
#                 initializers=[ignore_row],
#                 model=DeviceTestInfo,
#                 mapdict=mapdict)
#             messages.success(request, "导入成功")

#         except IntegrityError as e:
#             print(e)
#             messages.error(
#                 request, '导入失败：请检查Excel内容是否有以下错误: </br> 1.数据重复</br> 2.专业id不存在')
#         except ValueError as e:
#             print(e)
#             messages.error(
#                 request, '导入失败：请检查Excel内容是否有以下错误: </br> 1.数据格式错误 例如id类存在汉字或字母')
#         except Exception as e:
#             messages.error(request, str(e))
#         return JsonResponse({'msg': 'd'})
#     else:
#         pass