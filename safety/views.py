from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

# Create your views here.
from .models import SafetyFile
from .forms import SafetyFileForm


class SafetyFileListView(ListView):
    model = SafetyFile
    template_name = "TEMPLATE_NAME"

    def get_queryset(self):
        queryset = super(SafetyFileListView, self).get_queryset()
        if self.kwargs:
            queryset = queryset.filter(profess=self.kwargs.get('pro_id'))
        if self.request.GET.get('type_id'):
            queryset = queryset.filter(
                file_type=self.request.GET.get('type_id'))
        return queryset


class SafetyFileCreateView(CreateView):
    model = SafetyFile
    form_class = SafetyFileForm
    template_name = "TEMPLATE_NAME"


class SafetyFileUpdatView(UpdateView):
    model = SafetyFile
    form_class = SafetyFileForm

    template_name = "TEMPLATE_NAME"


class SafetyFileDeleteView(DeleteView):
    model = SafetyFile
    form_class = SafetyFileForm

    template_name = "TEMPLATE_NAME"


class SafetyFileDetailView(DetailView):
    model = SafetyFile
    form_class = SafetyFileForm
    template_name = "TEMPLATE_NAME"
