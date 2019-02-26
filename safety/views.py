from datetime import datetime

from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponse, redirect
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
