from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import transaction, IntegrityError
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteAjaxMixin
from django.contrib.messages.views import SuccessMessageMixin
import django_excel as excel

from .models import *
from .forms import  MaterialForm


class MaterialAddView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Material
    form_class = MaterialForm
    success_url = 'material:list'


class MaterialUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    success_url = 'material:list'


class MaterialDeleteView(DeleteAjaxMixin, DeleteView):
    model = Material
    form_class = MaterialForm
    success_url = 'material:list'


class MaterialListView(ListView):
    model = Material


class MaterialStockRecordView(ListView):
    model = Material


def material_in_out_stock(request, **kwargs):
    material = get_object_or_404(Material, pk=kwargs.get('pk'))
    in_or_out = int(request.POST.get('type'))  # 0 in 1 out
    count = int(request.POST.get('count'))
    try:
        with transaction.atomic():
            material.num += (count if not in_or_out else -count)
            material.objects.record_set.create(count=count, operation_type=type, create_user=request.user)
            material.save()
            return JsonResponse({'msg': 'ok'})
    except Exception as e:
        return JsonResponse({'msg': e})


def import_material_data(request):
    # 导入数据
    if request.method == "POST":
        try:
            request.FILES['docfile'].save_to_database(
                name_columns_by_row=0,
                model=Material,
                mapdict=['id', 'name', 'type_id', 'num', 'unit'])

            context = {
                'import_msg': 'ok'
            }

        except IntegrityError as e:
            print(e)
            context = {
                'import_msg': '请检查Excel是否与已有数据重复'
            }
        except ValueError as e:
            print(e)
            context = {
                'import_msg': '数据格式错误'
            }
        return JsonResponse(context)

    else:
        pass


def export_material_data(request):
    from datetime import datetime
    file_name = '物资表_'
    queryset = Material.objects.all()

    file_name += datetime.now().strftime("%Y-%m-%d")

    column_names = ['id', 'name', 'type_id', 'num', 'unit']
    colnames = ['物资编号', '名称', '型号', '数量', '单位']
    return excel.make_response_from_query_sets(
        queryset,
        column_names,
        'xls',
        file_name=file_name,
        colnames=colnames
    )
