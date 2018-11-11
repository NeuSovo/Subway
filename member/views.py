import django_excel as excel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView)

from .forms import *
from .models import *
from .utils import *


class LoginView(FormView):
    template_name = 'member/login.html'
    form_class = LoginForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                return self.form_valid(form, user)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, user=None):
        login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return render(request, 'member/login.html')


class AssignAccountView(CreateView):
    model = User
    template_name = "member/dept_assign_account_form.html"
    form_class = AssignAccountForm
    success_url = '/member/dept_assign_account_list/'

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return render(self.request, self.template_name, {'msg': 'no'})
        return super(AssignAccountView, self).dispatch(*args, **kwargs) 

    def post(self, request, *args, **kwargs):
        self.objects = None
        self.dept = get_object_or_404(Departments,pk=kwargs.get('dept_id', 0))
        self.success_url += str(self.dept.id)
        return super(AssignAccountView, self).post(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        self.objects = form.save()
        position = form.cleaned_data.get('position')
        # TODO: 对密码进行可逆性加密（*RSA*）
        enp = form.cleaned_data.get('password1')
        u = AssignAccount(user=self.objects, user_dept=self.dept, position=position, enp=enp)
        u.save()
        return super(AssignAccountView, self).form_valid(form, *args, **kwargs)


class AssignAccountListView(ListView):
    template_name = 'member/assign_account_list.html'
    model = AssignAccount

    def get(self, request, *args, **kwargs):
        self.dept = get_object_or_404(Departments, pk=kwargs.get('dept_id', 0))
        return super(AssignAccountListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(AssignAccountListView, self).get_queryset()
        queryset = queryset.filter(user_dept=self.dept)
        return queryset
    

class DeptListView(ListView):
    template_name = 'member/dept_list.html'
    model = Departments

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return render(self.request, self.template_name, {'msg': 'no'})
        return super(DeptListView, self).dispatch(*args, **kwargs) 

    def get_queryset(self):
        queryset = super(DeptListView, self).get_queryset()

        return queryset


class DeptCreateView(CreateView):
    model = Departments
    template_name = "member/dept_create_form.html"
    form_class = DeptCreateForm
    success_url = '/member/dept'

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return render(self.request, self.template_name, {'msg': 'no'})
        return super(DeptCreateView, self).dispatch(*args, **kwargs)


class DeptDeleteView(DeleteView):
    
    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return render(self.request, self.template_name, {'msg': 'no'})
        return super(DeptDeleteView, self).dispatch(*args, **kwargs)


class MemberAddView(CreateView):
    model = Member
    template_name = "member/member_add_form.html"
    form_class = MemberForm
    success_url = '/member/dept_assign_account_list/'

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        return super(MemberAddView, self).dispatch(*args, **kwargs)


class MemberListView(ListView):
    template_name = 'member/member_list.html'
    model = Member

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        return super(MemberListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        dept_id = self.request.GET.get('dept_id')
        self.dept = None

        if dept_id is None:
            if not request.user.is_superuser:
                self.dept = self.request.user.AssignAccount.user_dept
        else:
            if not request.user.is_superuser and dept_id != self.request.user.AssignAccount.user_dept_id:
                # TODO: xx
                pass
            else:
                self.dept = get_object_or_404(Departments, pk=dept_id)
       
        return super(MemberListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(MemberListView, self).get_queryset()
        if not self.dept:
            queryset = queryset
        else:
            queryset = queryset.filter(dept=self.dept)

        for i in queryset:
            setattr(i, 'qrcode', i.qrcode_content)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['dept_list'] = Departments.objects.all()
            context['select_dept'] = self.dept
        else:
            context['dept_list'] = self.request.user.AssignAccount.user_dept
            context['select_dept'] = self.dept
        return context


class MemberDetailView(DetailView):
    model = Member
    template_name = "member/member_detail.html"

    def get_object(self, queryset=None):
        try:
            self.kwargs[self.pk_url_kwarg] = de_base64(self.kwargs.get(self.pk_url_kwarg))
        except:
            raise 
        return super(MemberDetailView, self).get_object(queryset)
    
    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        setattr(context['object'], 'qrcode', context.get('object').qrcode_content)
        return context
    

def qrcode_view(request, data):
    img = gen_qrcode(data)
    response = HttpResponse(img, content_type="image/png")

    return response


def import_member_data(request):
    # 导入数据
    if request.method == "POST":
        try:
            request.FILES['docfile'].save_to_database(
                    name_columns_by_row=0,
                    model=Member,
                    mapdict=['member_id', 'dept_id', 'name', 'sex', 'birthday', 'position', 'phone'])
            
            context = {
                'import_msg': 'ok'
            }
        
        except IntegrityError as e:
            print (e)
            context = {
                'import_msg': '请检查Excel是否与已有数据重复'
            }
        except ValueError as e:
            print (e)
            context = {
                'import_msg': '数据格式错误'
            }
        return JsonResponse(context)

    else:  
        pass


def export_member_data(request, dept_id=None):
    from datetime import datetime
    file_name = '员工表_'
    if dept_id:
        dept = get_object_or_404(Departments, pk=dept_id)
        members = Member.objects.filter(dept_id=dept_id)
        file_name += dept.dept_name + '_'
    else:
        members = Member.objects.all()
    
    file_name += datetime.now().strftime("%Y-%m-%d")
    
    column_names  =['member_id', 'dept_id', 'get_dept_name', 'name', 'sex', 'birthday', 'position', 'phone']
    colnames=['员工工号','部门id','部门名字','姓名','性别','生日','职位', '电话']
    return excel.make_response_from_query_sets(
        members,
        column_names,
        'xls',
        file_name=file_name,
        colnames=colnames
    )
