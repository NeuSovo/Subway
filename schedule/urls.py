from django.urls import path
from .views import *

app_name = "schedule"
urlpatterns = [
    path('list', ScheduleFileListView.as_view(), name='list'),  # TODO
    path('add', ScheduleFileCreateView.as_view(), name='add'),
    path('update/<int:pk>', ScheduleFileUpdatView.as_view(), name='update'),
    path('delete/<int:pk>', ScheduleFileDetailView.as_view(), name='delete'),
]
