from django.urls import path
from .views import *

app_name = "material"
urlpatterns = [
    path('list', MaterialListView.as_view(), name='list'),
    path('list_profess/<int:profess_id>', MaterialListView.as_view(), name="list_profess"),

    path('add', MaterialAddView.as_view(), name='add'),
    path('update/<int:pk>', MaterialUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', MaterialDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>', MaterialDetailView.as_view(), name='detail'),
    path('import', import_material_data, name='import'),
    path('export', export_material_data, name='export'),
    path('export_qr', export_qr, name='export_qr'),

    path('stock/record', MaterialStockRecordView.as_view(), name='stock_record'),
    path('stock/record/<int:pk>', MaterialStockRecordView.as_view(), name='stock_record_with_id'),
    path('stock/in_out/<int:pk>', material_in_out_stock, name='in_out_stock'),

    path('init_profess', ProfessInitView.as_view(), name='init_profess'),
    path('add_profess', ProfessCreateView.as_view(), name='add_profess'),
    path('update_profess/<int:pk>', ProfessUpdateView.as_view(), name='update_profess'),
    path('delete_profess/<int:pk>', ProfessDeleteView.as_view(), name='delete_profess'),
         path('qr1', QR1),
     path('qr2/<int:profess_id>', QR2)
]
