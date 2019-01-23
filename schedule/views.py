from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


# Create your views here.


class ScheduleFileListView(ListView):
    template_name = "Schedule/Schedule.html"


class ScheduleFileCreateView(CreateView):
    template_name = "TEMPLATE_NAME"


class ScheduleFileUpdatView(UpdateView):
    template_name = "TEMPLATE_NAME"


class ScheduleFileDeleteView(DeleteView):
    template_name = "TEMPLATE_NAME"


class ScheduleFileDetailView(DetailView):
    template_name = "TEMPLATE_NAME"
