from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView


# Create your views here.


class DeviceFileListView(TemplateView):
    template_name = "device/device.html"


class DeviceDetialView(TemplateView):
    template_name = "device/device_detail.html"


class DeviceFileCreateView(TemplateView):
    template_name = "device/add_update_form.html"


class DeviceFileUpdatView(UpdateView):
    template_name = "TEMPLATE_NAME"


class DeviceFileDeleteView(DeleteView):
    template_name = "TEMPLATE_NAME"


class DeviceFileDetailView(DetailView):
    template_name = "TEMPLATE_NAME"


class QrCodeView(TemplateView):
    template_name = "setting/setting_qr.html"


class FrontendView(TemplateView):
    template_name = "setting/setting_fronted.html"


class BackendView(TemplateView):
    template_name = "setting/setting_backend.html"
