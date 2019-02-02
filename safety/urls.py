from django.urls import path
from .views import *

app_name = "safety"
urlpatterns = [
    path('list', SafetyFileListView.as_view(), name='list'),    # TODO
    path('add', SafetyFileCreateView.as_view(), name='add'),
    path('update/<int:pk>', SafetyFileUpdatView.as_view(), name='update'),
    path('delete/<int:pk>', SafetyFileDetailView.as_view(), name='delete'),
]
