from django.urls import path
from .views import *

app_name = "technology"
urlpatterns = [
    path('list', TechnologyFileListView.as_view(), name='list'),    # TODO
    path('list/<int:pro_id>', TechnologyFileListView.as_view(), name='list_with_id'),    # TODO

    path('add', TechnologyFileCreateView.as_view(), name='add'),
    path('update/<int:pk>', TechnologyFileUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', TechnologyFileDeleteView.as_view(), name='delete'),
]
