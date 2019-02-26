from datetime import datetime

import django_excel as excel
from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponse, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from core.utils import compress_file

from .forms import SafetyFileForm
from .models import *


class SafetyFileListView(ListView):
    model = SafetyFile
    template_name = "safety/safe.html"

    def get(self, request, *args, **kwargs):
        self.type = kwargs.get('type_id')

        if (self.type is not None and self.type >= len(self.model.file_type_choiced)):
            raise Http404

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(SafetyFileListView, self).get_queryset()
        if self.type is not None:
            queryset = queryset.filter(file_type=self.type)
            self.type = self.model.file_type_choiced[self.type][1]
        else:
            self.type = '全部'
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['type_s'] = self.model.file_type_choiced
        context['select_type'] = self.type
        return context


class SafetyFileCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = SafetyFile
    form_class = SafetyFileForm
    template_name = "safety/add_update_form.html"
    success_url = reverse_lazy('safety:list')


class SafetyFileUpdatView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = SafetyFile
    form_class = SafetyFileForm

    template_name = "safety/add_update_form.html"
    success_url = reverse_lazy('safety:list')


class SafetyFileDeleteView(DeleteAjaxMixin, DeleteView):
    model = SafetyFile
    form_class = SafetyFileForm
    success_message = '删除成功'
    template_name = "safety/delete_form.html"
    success_url = reverse_lazy('safety:list')


class SafetyFileDetailView(DetailView):
    model = SafetyFile

    def get(self, request, *args, **kwargs):
        return redirect(self.get_object().file_s.url)


def export_qr(request, dept_id=None):
    file_name = '安全二维码_'
    qr = SafetyFile.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d") + '.zip'
    s = compress_file([os.path.join(QR_DIR, QR_NAME_TEM % i.id) for i in qr])
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=" + \
        file_name.encode('utf-8').decode('ISO-8859-1')
    s.seek(0)
    response.write(s.read())
    return response


def import_safety_data(request):
    # 导入数据
    mapdict = {
        "标题": 'title',
        "文件类型id": 'file_type'
    }
    if request.method == "POST":
        try:
            request.FILES['docfile'].save_to_database(
                name_columns_by_row=0,
                model=SafetyFile,
                mapdict=mapdict)
            messages.success(request, "导入成功")

        except IntegrityError as e:
            print(e)
            messages.error(
                request, '导入失败：请检查Excel内容是否有以下错误: </br> 1.数据重复</br> 2.id不存在')
        except ValueError as e:
            print(e)
            messages.error(
                request, '导入失败：请检查Excel内容是否有以下错误: </br> 1.数据格式错误 例如id类存在汉字或字母')
        except Exception as e:
            messages.error(request, str(e))
        return JsonResponse({'msg': 'd'})

    else:
        pass


def export_safety_data(request):
    file_name = '安全文件表_'
    safetys = SafetyFile.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d")

    column_names = ['id', 'title', 'file_type', 'type_display']
    colnames = ['编号', '标题', '文件类型id', '类型名称' ]
    return excel.make_response_from_query_sets(
        safetys,
        column_names,
        'xls',
        file_name=file_name,
        colnames=colnames,
    )
