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
        queryset = queryset  # TODO
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
