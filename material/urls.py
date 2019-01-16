from django.urls import path
from .views import *

app_name = "material"
urlpatterns = [
    path('list', MaterialListView.as_view(), name='list'),
    path('add', MaterialAddView.as_view(), name='add'),
    path('update/<int:pk>', MaterialUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', MaterialDeleteView.as_view(), name='delete'),
    path('import', import_material_data, name='import'),
    path('export', export_material_data, name='export'),

    path('stock/record', MaterialStockRecordView.as_view(), name='stock_record'),
    path('stock/record/<int:pk>', MaterialStockRecordView.as_view(), name='stock_record_with_id'),
    path('stock/in_out/<int:pk>', material_in_out_stock, name='in_out_stock'),
]
