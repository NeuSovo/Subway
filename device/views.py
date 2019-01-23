from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


# Create your views here.


class DeviceFileListView(ListView):
    template_name = "device/device.html"


class DeviceFileCreateView(CreateView):
    template_name = "TEMPLATE_NAME"


class DeviceFileUpdatView(UpdateView):
    template_name = "TEMPLATE_NAME"


class DeviceFileDeleteView(DeleteView):
    template_name = "TEMPLATE_NAME"


class DeviceFileDetailView(DetailView):
    template_name = "TEMPLATE_NAME"
