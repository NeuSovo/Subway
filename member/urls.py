from django.urls import path
from .views import *

app_name = "member"
urlpatterns = [

    path('', index),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/login_mobile', MobieLoginViw.as_view(), name='login_mobile'),
    path('auth/logout', logout_view, name='logout'),
    path('index', IndexView.as_view(), name="index"),
    path('auth/index', IndexView2, name="index2"),
    path('global/qrcode/<path:data>', qrcode_view, name='qrcode'),
    path('global/success', success_view, name='success'),
    path('global/depass', depass_view, name='depass'),
    path('member/member_add', MemberAddView.as_view(), name='member_add'),
    path('member/member_list', MemberListView.as_view(), name='member_list'),
    path('member/member_update/<int:pk>', MemberUpdateView.as_view(), name='member_update'),
    path('member/member_delete/<int:pk>', MemberDeleteView.as_view(), name='member_delete'),
    path('member/member_list_detail', MemberListDetailView.as_view(), name='member_list_detail'),
    path('member/member_list_detail/<int:dept_id>', MemberListDetailView.as_view(), name='member_list_detail_with_id'),
    path('member/member_list/<int:dept_id>', MemberListView.as_view(), name='member_list_with_id'),
    path('member/member_import', import_member_data, name='member_import'),
    path('member/member_export', export_member_data, name='member_export'),
    path('member/member_export/<int:dept_id>', export_member_data, name='member_export_with_id'),
    path('member/member_detail/<str:pk>', MemberDetailView.as_view(), name='member_detail'),
    path('member/dept', DeptListView.as_view(), name='dept_list'),
    path('member/dept_create', DeptCreateView.as_view(), name='dept_create'),
    path('member/dept_update/<int:pk>', DeptUpdateView.as_view(), name='dept_update'),
    path('member/dept_delete/<int:pk>', DeptDeleteView.as_view(), name='dept_delete'),
    path('member/dept_assign_account/<int:pk>', AssignAccountView.as_view(), name='dept_assign_account'),
    path('member/dept_assign_account/update/<int:pk>', AssignAccountUpdateView.as_view(), name='update_assign_account'),
    path('member/dept_assign_account/delete/<int:pk>', AssignAccountDeleteView.as_view(), name='delete_assign_account'),
    path('member/dept_assign_account_list', AssignAccountListView.as_view(), name='dept_assign_account_list'),
    path('member/dept_assign_account_list/<int:dept_id>', AssignAccountListView.as_view(), name='accout_list_with_id'),

    path('member/export_qr/<int:dept_id>', export_qr_with_dept, name='export_qr_with_dept')
]
