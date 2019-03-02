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

from core.utils import compress_file
from core.QR import make_qr_pic

from .forms import MaterialForm, ProfessForm
from .models import *


class MaterialAddView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'material/material_create_form.html'
    success_url = reverse_lazy('material:list')
    success_message = '%(name)s 添加成功'


class MaterialUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'material/material_update_form.html'
    success_url = reverse_lazy('material:list')
    success_message = '%(name)s 更新成功'


class MaterialDetailView(DetailView):
    model = Material
    template_name = "material/material_mobile.html"


class MaterialDeleteView(DeleteAjaxMixin, DeleteView):
    model = Material
    form_class = MaterialForm
    template_name = 'material/material_delete_form.html'
    success_url = reverse_lazy('material:list')
    success_message = '删除成功'


class MaterialListView(ListView):
    model = Material
    template_name = 'material/material.html'
    paginate_by = 100

    def __init__(self):
        super().__init__()
        self.profess_all = Profess.objects.all()
        self.profess = self.profess_all[0] if len(self.profess_all) > 0 else 0

    def get(self, request, *args, **kwargs):
        if not self.profess:
            return HttpResponseRedirect(reverse_lazy('material:init_profess'))
        profess_id = kwargs.get('profess_id')
        if profess_id:
            self.profess = get_object_or_404(Profess, pk=profess_id)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(MaterialListView, self).get_queryset()
        queryset = queryset.filter(profess=self.profess)
        print(len(queryset))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profess_s'] = self.profess_all
        context['select_profess'] = self.profess
        return context


class MaterialStockRecordView(ListView):
    model = MaterialStock
    template_name = 'material/material_record.html'

    def get(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk', 0)
        return super(MaterialStockRecordView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(MaterialStockRecordView, self).get_queryset()
        if self.pk:
            queryset = queryset.filter(material_id=self.pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MaterialStockRecordView,
                        self).get_context_data(**kwargs)
        context['material_list'] = Material.objects.all()
        if self.pk:
            context['select_material'] = get_object_or_404(
                Material, pk=self.pk)
        else:
            context['select_material'] = '全部'
        return context


class ProfessCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "material/add_update_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('material:list')


class ProfessInitView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "material/init_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('material:list')


class ProfessUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Profess
    form_class = ProfessForm
    template_name = "material/add_update_profess_form.html"
    success_message = '%(name)s 更新成功'
    success_url = reverse_lazy('material:list')


class ProfessDeleteView(DeleteView):
    model = Profess
    form_class = ProfessForm
    success_message = '%(name)s 删除成功'
    template_name = "material/delete_profess.html"
    success_url = reverse_lazy('material:list')


def material_in_out_stock(request, **kwargs):
    material = get_object_or_404(Material, pk=kwargs.get('pk'))
    in_or_out = int(request.POST.get('type_id'))  # 0 in 1 out
    count = int(request.POST.get('count'))
    try:
        with transaction.atomic():
            material.num += count if not in_or_out else -count
            material.record.create(
                count=count, operation_type=in_or_out, create_user=request.user)
            material.save()
            return JsonResponse({'msg': 'ok'})
    except Exception as e:
        # raise e
        return JsonResponse({'msg': str(e)})


def import_material_data(request):
    # 导入数据
    mapdict = {
        "名称": "name",
        "生产厂家": "manufacturer",
        "专业id": "profess_id",
        '型号': 'type_id',
        '数量': 'num',
        '单位': 'unit',
    }
    if request.method == "POST":
        try:
            request.FILES['docfile'].save_to_database(
                name_columns_by_row=0,
                model=Material,
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


def export_material_data(request):
    file_name = '物资表_'
    queryset = Material.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d")

    column_names = ['id', 'name', 'manufacturer',
                    'profess_id', 'profess_name', 'type_id', 'num', 'unit']
    colnames = ['物资编号', '名称', '生产厂家', '专业id', '专业名称', '型号', '数量', '单位']
    return excel.make_response_from_query_sets(
        queryset,
        column_names,
        'xls',
        file_name=file_name,
        colnames=colnames,
        sheet_name='物资数据',
    )


def export_qr(request, dept_id=None):
    file_name = '物资二维码_'
    qr = Material.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d") + '.zip'
    s = compress_file(
        [os.path.join(QR_DIR_3, QR_3_NAME_TEM % i.id) for i in qr])
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=" + \
                                      file_name.encode('utf-8').decode('ISO-8859-1')
    s.seek(0)
    response.write(s.read())
    return response


def QR1(request):
    
    profess_s = Profess.objects.all()
    context = {
        'profess_s': profess_s,
        'title': '物资信息',
        'url': '/material/qr2/'

    }
    return render(request, 'system/profess_mobile.html', context=context)

def QR2(request, profess_id):
    profess = get_object_or_404(Profess, pk=profess_id)

    queryset =  Material.objects.filter(profess=profess)
    context = {
        'object_list': queryset,
        'select_profess': profess,
        'title': '物资信息',
        'url': '/material/detail/'
    }
    return render(request, 'system/professs_mobile.html', context=context)


def qr1_make(request):
    img = make_pic(['物资信息', '全部专业'], '/meterial/qr1')
    img.save('test.png')
    try:
        with open('test.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except Exception as e:
        raise e
