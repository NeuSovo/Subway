from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import transaction, IntegrityError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteAjaxMixin
from django.contrib.messages.views import SuccessMessageMixin
import django_excel as excel

from .models import *
from .forms import MaterialForm


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



class MaterialDeleteView(DeleteAjaxMixin, DeleteView):
    model = Material
    form_class = MaterialForm
    template_name = 'material/material_delete_form.html'
    success_url = reverse_lazy('material:list')


class MaterialListView(ListView):
    model = Material
    template_name = 'material/material.html'
    paginate_by = 100


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
        context = super(MaterialStockRecordView, self).get_context_data(**kwargs)
        context['material_list'] = Material.objects.all()
        if self.pk:
            context['select_material'] = get_object_or_404(Material, pk=self.pk)
        else:
            context['select_material'] = '全部'
        return context


def material_in_out_stock(request, **kwargs):
    material = get_object_or_404(Material, pk=kwargs.get('pk'))
    in_or_out = int(request.POST.get('type_id'))  # 0 in 1 out
    count = int(request.POST.get('count'))
    print(material, in_or_out, count, type(request.user))
    try:
        with transaction.atomic():
            material.num += count if not in_or_out else -count
            material.record.create(count=count, operation_type=in_or_out, create_user=request.user)
            material.save()
            return JsonResponse({'msg': 'ok'})
    except Exception as e:
        # raise e
        return JsonResponse({'msg': str(e)})


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
