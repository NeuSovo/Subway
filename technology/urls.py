from django.urls import path
from .views import *

app_name = "technology"
urlpatterns = [
    path('list', TechnologyFileListView.as_view(), name='list'),
    path('list/<int:profess_id>',
         TechnologyFileListView.as_view(), name='list_profess'),
    path('list/<int:profess_id>/<int:type_id>',
         TechnologyFileListView.as_view(), name='list_type'),

    path('add', TechnologyFileCreateView.as_view(), name='add'),
    path('update/<int:pk>', TechnologyFileUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', TechnologyFileDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>', TechnologyFileDetailView.as_view(), name='detail'),
    path('init_profess', ProfessInitView.as_view(), name='init_profess'),
    path('add_profess', ProfessCreateView.as_view(), name='add_profess'),
    path('update_profess/<int:pk>',
         ProfessUpdateView.as_view(), name='update_profess'),
    path('delete_profess/<int:pk>',
         ProfessDeleteView.as_view(), name='delete_profess'),
    path('export_qr', export_qr, name='export_qr'),

    path('import', import_technology_data, name='import'),
    path('export', export_technology_data, name='export'),
    path('qr1', QR1),
    path('qr2/<int:profess_id>', QR2),
    path('qr1_make', qr1_make, name='qr1_make')


]
