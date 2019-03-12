# -*- coding: utf-8 -*-  

from datetime import datetime

import django_excel as excel
from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, render)
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from core.utils import compress_file
from urllib.parse import quote
from .forms import ProfessForm, TechnologyFileForm
from .models import *


class TechnologyFileListView(ListView):
    model = TechnologyFile
    template_name = "technology/technology.html"

    def __init__(self):
        super().__init__()
        self.profess_all = Profess.objects.all()
        self.profess = self.profess_all[0] if len(self.profess_all) > 0 else 0

        self.type = None

    def get(self, request, *args, **kwargs):
        if not self.profess:
            return HttpResponseRedirect(reverse_lazy('technology:init_profess'))
        profess_id = kwargs.get('profess_id')
        if profess_id:
            self.profess = get_object_or_404(Profess, pk=profess_id)
        self.type = kwargs.get('type_id')

        if (self.type is not None and self.type >= len(self.model.file_type_choiced)):
            raise Http404

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(TechnologyFileListView, self).get_queryset()
        queryset = queryset.filter(profess=self.profess)
        if self.type is not None:
            queryset = queryset.filter(file_type=self.type)
            self.type = self.model.file_type_choiced[self.type][1]
        else:
            self.type = '全部'
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profess_s'] = self.profess_all
        context['select_profess'] = self.profess
        context['select_type'] = self.type
        return context


class TechnologyFileCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = TechnologyFile
    form_class = TechnologyFileForm
    template_name = "technology/add_update_form.html"
    success_message = '添加成功'
    success_url = reverse_lazy('technology:list')


class TechnologyFileUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = TechnologyFile
    form_class = TechnologyFileForm
    template_name = "technology/add_update_form.html"
    success_message = '修改成功'
    success_url = reverse_lazy('technology:list')

    def post(self, request, **args):
        self.success_url = request.META.get('HTTP_REFERER') or self.success_url
        return super().post(request, *args)

    def form_valid(self, form, **args):
        self.object.gen_qrcode_img()
        return super().form_valid(form, **args)


class TechnologyFileDetailView(DetailView):
    model = TechnologyFile
    template_name = "technology/technology_mobile.html"


class TechnologyFileDeleteView(DeleteAjaxMixin, DeleteView):
    model = TechnologyFile
    form_class = TechnologyFileForm
    template_name = "technology/delete_form.html"
    success_message = '删除成功'
    success_url = reverse_lazy('technology:list')


class ProfessCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "technology/add_update_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('technology:list')


class ProfessInitView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "technology/init_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('technology:list')


class ProfessUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Profess
    form_class = ProfessForm
    template_name = "technology/add_update_profess_form.html"
    success_message = '%(name)s 更新成功'
    success_url = reverse_lazy('technology:list')

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
    template_name = "technology/delete_profess.html"
    success_url = reverse_lazy('technology:list')


def export_qr(request, dept_id=None):
    file_name = '技术二维码_'
    qr = TechnologyFile.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d") + '.zip'
    s = compress_file(
        [os.path.join(QR_DIR_3, QR_3_NAME_TEM % i.id) for i in qr])
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename={}".format(quote(file_name))
    s.seek(0)
    response.write(s.read())
    return response


def import_technology_data(request):
    # 导入数据
    mapdict = {
        "标题": 'title',
        "文件类型id": 'file_type',
        '专业id': 'profess_id'
    }
    if request.method == "POST":
        try:
            request.FILES['docfile'].save_to_database(
                name_columns_by_row=0,
                model=TechnologyFile,
                mapdict=mapdict,
                ignore_cols_at_names=['编号', '类型名称', '专业名称'])
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


def export_technology_data(request):
    file_name = '技术文件表_'
    techs = TechnologyFile.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d")

    column_names = ['id', 'title', 'file_type',
                    'type_display', 'profess_id', 'profess_name', ]
    colnames = ['编号', '标题', '文件类型id', '类型名称', '专业id', '专业名称', ]
    return excel.make_response_from_query_sets(
        techs,
        column_names,
        'xls',
        file_name=file_name,
        colnames=colnames,
        ignore_rows = [0] if len(techs) else [1]
    )


def QR1(request):
    
    profess_s = Profess.objects.all()
    context = {
        'profess_s': profess_s,
        'title': '技术信息',
        'url': '/technology/qr2/'

    }
    return render(request, 'system/profess_mobile.html', context=context)


def QR2(request, profess_id):
    profess = get_object_or_404(Profess, pk=profess_id)

    queryset = TechnologyFile.objects.filter(profess=profess)
    context = {
        'object_list': queryset,
        'select_profess': profess,
        'title': '技术信息',
        'url': '/technology/detail/'
    }
    return render(request, 'system/professs_mobile.html', context=context)


def qr1_make(request):
    img = make_pic(['技术信息', '全部专业'], '/technology/qr1')
    img.save('test.png')
    try:
        with open('test.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except Exception as e:
        raise e
