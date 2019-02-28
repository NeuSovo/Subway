from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, render)
from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from .models import *
from .forms import ProfessForm, DeviceForm, DeviceTestInfoForm


class DeviceAddView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_create_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '%(name)s 添加成功'


class DeviceTestInfoUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = DeviceTestInfo
    form_class = DeviceTestInfoForm
    template_name = 'device/device_create_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '更新成功'


class DeviceUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_update_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '%(name)s 更新成功'


class DeviceDetailView(DetailView):
    model = Device
    template_name = "device/device_mobile.html"


class DeviceDeleteView(DeleteAjaxMixin, DeleteView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_delete_form.html'
    success_url = reverse_lazy('device:list')
    success_message = '删除成功'


class DeviceListView(ListView):
    model = Device
    template_name = 'device/device.html'
    paginate_by = 100

    def __init__(self):
        super().__init__()
        self.profess_all = Profess.objects.all()
        self.profess = self.profess_all[0] if len(self.profess_all) > 0 else 0

    def get(self, request, *args, **kwargs):
        if not self.profess:
            return HttpResponseRedirect(reverse_lazy('device:init_profess'))
        profess_id = kwargs.get('profess_id')
        if profess_id:
            self.profess = get_object_or_404(Profess, pk=profess_id)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(DeviceListView, self).get_queryset()
        queryset = queryset.filter(profess=self.profess)
        print(len(queryset))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profess_s'] = self.profess_all
        context['select_profess'] = self.profess
        return context


class DeviceListDetailView(DeviceListView):
    template_name = 'device/device_list_detail.html'
    pass


class ProfessCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "device/add_update_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('device:list')


class ProfessInitView(PassRequestMixin, SuccessMessageMixin, CreateView):
    model = Profess
    form_class = ProfessForm
    template_name = "device/init_profess_form.html"
    success_message = '%(name)s 添加成功'
    success_url = reverse_lazy('device:list')


class ProfessUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Profess
    form_class = ProfessForm
    template_name = "device/add_update_profess_form.html"
    success_message = '%(name)s 更新成功'
    success_url = reverse_lazy('device:list')


class ProfessDeleteView(DeleteView):
    model = Profess
    form_class = ProfessForm
    success_message = '%(name)s 删除成功'
    template_name = "device/delete_profess.html"
    success_url = reverse_lazy('device:list')


def QR1(request):
    
    profess_s = Profess.objects.all()
    context = {
        'profess_s': profess_s,
        'title': '设备信息',
        'url': '/device/qr2/'

    }
    return render(request, 'system/profess_mobile.html', context=context)


def QR2(request, profess_id):
    profess = get_object_or_404(Profess, pk=profess_id)

    queryset = Device.objects.filter(profess=profess)
    context = {
        'object_list': queryset,
        'select_profess': profess,
        'title': '设备信息',
        'url': '/device/detail/'
    }
    return render(request, 'system/professs_mobile.html', context=context)


def qr1_make(request):
    img = make_pic(['设备信息', '全部专业'], '/device/qr1')
    img.save('test.png')
    try:
        with open('test.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except Exception as e:
        raise e
