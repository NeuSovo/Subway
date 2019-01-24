from django.shortcuts import render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import TechnologyFile
from .forms import TechnologyFileForm
from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteAjaxMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class TechnologyFileListView(ListView):
    model = TechnologyFile
    template_name = "technology/technology.html"

    def __init__(self):
        super().__init__()
        self.profess = 0
        self.type = None

    def get(self, request, *args, **kwargs):
        self.profess = kwargs.get('profess') or self.profess
        self.type = kwargs.get('type')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(TechnologyFileListView, self).get_queryset()
        queryset = queryset.filter(profess=self.profess)
        if self.type or self.type == 0:
            queryset = queryset.filter(file_type=self.type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
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

