from django.shortcuts import render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import TechnologyFile
from .forms import TechnologyFileForm


class TechnologyFileListView(ListView):
    model = TechnologyFile
    template_name = "TEMPLATE_NAME"

    def get_queryset(self):
        queryset = super(TechnologyFileListView, self).get_queryset()
        if self.kwargs:
            queryset = queryset.filter(profess=self.kwargs.get('pro_id'))
        if self.request.GET.get('type_id'):
            queryset = queryset.filter(
                file_type=self.request.GET.get('type_id'))
        return queryset


class TechnologyFileCreateView(CreateView):
    model = TechnologyFile
    form_class = TechnologyFileForm
    template_name = "TEMPLATE_NAME"


class TechnologyFileUpdateView(UpdateView):
    model = TechnologyFile
    form_class = TechnologyFileForm
    template_name = "TEMPLATE_NAME"


class TechnologyFileDetailView(DetailView):
    model = TechnologyFile
    template_name = "TEMPLATE_NAME"


class TechnologyFileDeleteView(DeleteView):
    model = TechnologyFile
    form_class = TechnologyFileForm
    template_name = "TEMPLATE_NAME"
