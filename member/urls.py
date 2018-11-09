from django.urls import path
from .views import *

app_name = "member"
urlpatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('member/dept', DeptListView.as_view(), name='dept_list'),
    path('member/dept_create',DeptCreateView.as_view(), name='dept_create')
]
