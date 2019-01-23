from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView


# Create your views here.


class ScheduleListView(TemplateView):
    template_name = "schedule/schedule.html"


class ScheduleDetailView(TemplateView):
    template_name = "schedule/schedule_detail.html"


class ScheduleChartView(TemplateView):
    template_name = "schedule/schedule_chart.html"


class ScheduleItemChartView(TemplateView):
    template_name = "schedule/schedule_item.html"


class ScheduleFileCreateView(CreateView):
    template_name = "TEMPLATE_NAME"


class ScheduleFileUpdatView(UpdateView):
    template_name = "TEMPLATE_NAME"


class ScheduleFileDeleteView(DeleteView):
    template_name = "TEMPLATE_NAME"


class ScheduleFileDetailView(DetailView):
    template_name = "TEMPLATE_NAME"
