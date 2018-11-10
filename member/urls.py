from django.urls import path
from .views import *

app_name = "member"
urlpatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('member/dept', DeptListView.as_view(), name='dept_list'),

    path('member/member_add', MemberAddView.as_view(), name='member_add'),
    path('member/member_list', MemberListView.as_view(), name='member_list'),


    path('member/dept_create',DeptCreateView.as_view(), name='dept_create'),
    path('member/dept_assign_account/<int:dept_id>', AssignAccountView.as_view(), name='dept_assign_account'),
    path('member/dept_assign_account_list/<int:dept_id>', AssignAccountListView.as_view(), name='dept_assign_account_list')
]
