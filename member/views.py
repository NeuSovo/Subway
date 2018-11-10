from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, FormView, ListView, DetailView

from .forms import *
from .models import *


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


def logout(request):
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

    


def import_member_data(request):
    # 导入数据
    pass