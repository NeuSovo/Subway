from django.urls import path
from .views import *

app_name = "material"
urlpatterns = [
    path('material/list', MaterialListView.as_view(), name='list'),
    path('material/add', MaterialAddView.as_view(), name='add'),
    path('material/update', MaterialUpdateView.as_view(), name='update'),
    path('material/delete', MaterialDeleteView.as_view(), name='delete'),
    path('material/import', import_material_data, name='import'),
    path('material/export', export_material_data, name='export'),

    path('material/stock/record', MaterialStockRecordView.as_view(), name='stock_record'),
    path('material/stock/in_out/<int:pk>', material_in_out_stock, name='in_out_stock'),
]
