from django.urls import path
from .views import *

app_name = "device"
urlpatterns = [
    path('list', DeviceFileListView.as_view(), name='list'),    # TODO
    path('add', DeviceFileCreateView.as_view(), name='add'),
    path('update/<int:pk>', DeviceFileUpdatView.as_view(), name='update'),
    path('delete/<int:pk>', DeviceFileDetailView.as_view(), name='delete'),
]
