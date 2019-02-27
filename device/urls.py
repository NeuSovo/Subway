from django.urls import path
from .views import *

app_name = "device"
urlpatterns = [
    path('list', DeviceListView.as_view(), name='list'),
    path('list_detail', DeviceListDetailView.as_view(), name='list_detail'),
    path('list_profess/<int:profess_id>', DeviceListView.as_view(), name="list_profess"),
    path('list_detail_profess/<int:profess_id>', DeviceListDetailView.as_view(), name='list_detail_profess'),

    path('detail', DeviceDetailView.as_view(), name='detail'),
    path('add', DeviceAddView.as_view(), name='add'),
    path('update/<int:pk>', DeviceUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', DeviceDeleteView.as_view(), name='delete'),

    path('init_profess', ProfessInitView.as_view(), name='init_profess'),
    path('add_profess', ProfessCreateView.as_view(), name='add_profess'),
    path('update_profess/<int:pk>', ProfessUpdateView.as_view(), name='update_profess'),
    path('delete_profess/<int:pk>', ProfessDeleteView.as_view(), name='delete_profess'),

    path('update_test_device/<int:pk>', DeviceTestInfoUpdateView.as_view(), name='update_test_device')
]
