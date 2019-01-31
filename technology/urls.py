from django.urls import path
from .views import *

app_name = "technology"
urlpatterns = [
    path('list', TechnologyFileListView.as_view(), name='list'),
    path('list/<int:profess_id>', TechnologyFileListView.as_view(), name='list_profess'),
    path('list/<int:profess_id>/<int:type_id>', TechnologyFileListView.as_view(), name='list_type'),

    path('add', TechnologyFileCreateView.as_view(), name='add'),
    path('update/<int:pk>', TechnologyFileUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', TechnologyFileDeleteView.as_view(), name='delete'),
]
