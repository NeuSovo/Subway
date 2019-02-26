from datetime import datetime

from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, render)
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from core.utils import compress_file

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


class TechnologyFileDetailView(DetailView):
    model = TechnologyFile
    template_name = "TEMPLATE_NAME"


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
    response["Content-Disposition"] = "attachment; filename=" + \
        file_name.encode('utf-8').decode('ISO-8859-1')
    s.seek(0)
    response.write(s.read())
    return response
