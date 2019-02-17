from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from .models import SafetyFile
from .forms import SafetyFileForm


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
        print (self.model.file_type_choiced)
        context['type_s'] = self.model.file_type_choiced
        context['select_type'] = self.type
        return context



class SafetyFileCreateView(CreateView):
    model = SafetyFile
    form_class = SafetyFileForm
    template_name = "safety/add_update_form.html"
    success_url = reverse_lazy('safety:list')



class SafetyFileUpdatView(UpdateView):
    model = SafetyFile
    form_class = SafetyFileForm

    template_name = "safety/add_update_form.html"
    success_url = reverse_lazy('safety:list')



class SafetyFileDeleteView(DeleteView):
    model = SafetyFile
    form_class = SafetyFileForm

    template_name = "safety/delete_form.html"
    success_url = reverse_lazy('safety:list')



class SafetyFileDetailView(DetailView):
    model = SafetyFile
    form_class = SafetyFileForm
    template_name = "safety/delete_form.html"
