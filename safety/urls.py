from django.urls import path
from .views import *

app_name = "safety"
urlpatterns = [
    path('list', SafetyFileListView.as_view(), name='list'),    # TODO
    path('list/<int:type_id>', SafetyFileListView.as_view(), name='list_with_type'),
    path('add', SafetyFileCreateView.as_view(), name='add'),
    path('update/<int:pk>', SafetyFileUpdatView.as_view(), name='update'),
    path('delete/<int:pk>', SafetyFileDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>', SafetyFileDetailView.as_view(), name='detail'),
    path('export_qr', export_qr, name='export_qr'),

]
