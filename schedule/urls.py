from django.urls import path
from .views import *

app_name = "schedule"
urlpatterns = [
    path('list', ScheduleListView.as_view(), name='list'),
    path('list_detail', ScheduleListDetailView.as_view(), name='list_detail'),
    path('list_profess/<int:profess_id>', ScheduleListView.as_view(), name="list_profess"),
    path('list_detail/<int:profess_id>', ScheduleListDetailView.as_view(), name='list_detail_with_profess'),
    path('list_chart', ScheduleListChartView.as_view(), name='list_chart'),
    path('list_chart/<int:profess_id>', ScheduleListChartView.as_view(), name='list_chart_with_profess'),

    path('add', ScheduleAddView.as_view(), name='add'),
    path('update/<int:pk>', ScheduleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ScheduleDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>', ScheduleDetailView.as_view(), name='detail'),
    path('item_chart/<int:pk>', ScheduleItemChartView.as_view(), name='item_chart'),

    path('mobile/<int:pk>', ScheduleItemMobileView.as_view(), name='mobile_item'),
    path('mobile', ScheduleListMobileView.as_view(), name='mobile'),

    path('init_profess', ProfessInitView.as_view(), name='init_profess'),
    path('add_profess', ProfessCreateView.as_view(), name='add_profess'),
    path('update_profess/<int:pk>', ProfessUpdateView.as_view(), name='update_profess'),
    path('delete_profess/<int:pk>', ProfessDeleteView.as_view(), name='delete_profess'),
    path('qr1', QR1),
    path('qr2/<int:profess_id>', QR2)
]
