from django.urls import path
from .views import *

app_name = "schedule"
urlpatterns = [
    path('list', ScheduleListView.as_view(), name='list'),
    path('detail', ScheduleDetailView.as_view(), name='detail'),
    path('chart', ScheduleChartView.as_view(), name='chart'),
    path('item', ScheduleItemChartView.as_view(), name='item'),
    path('add', ScheduleFileCreateView.as_view(), name='add'),
    path('update/<int:pk>', ScheduleFileUpdatView.as_view(), name='update'),
    path('delete/<int:pk>', ScheduleFileDetailView.as_view(), name='delete'),
]
