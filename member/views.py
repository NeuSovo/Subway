import django_excel as excel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, UpdateView, DeleteView, DetailView, FormView,
                                  ListView, View)
from bootstrap_modal_forms.mixins import PassRequestMixin
from .forms import *
from .models import *
from core.utils import *
from core.init_permission import *


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
                init_permission(user, request)
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
    return redirect('/')


class AssignAccountView(View):
    model = Account

    # template_name = "member/dept_assign_account_form.html"
    # form_class = AssignAccountForm
    # success_url = '/member/dept_assign_account_list/'

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return render(self.request, self.template_name, {'msg': 'no'})
        return super(AssignAccountView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        dept = get_object_or_404(Departments, pk=kwargs.get('dept_id', 0))
        obj = data_to_obj(self.model, request.POST)
        try:
            # TODO: 封装
            with transaction.atomic():
                obj.user_dept = dept
                obj.position = request.POST.get('position', '无')
                obj.enp = obj.password
                obj.set_password(obj.password)
                obj.save()
                obj.add_role(request.POST.getlist('role'))
                return JsonResponse({'msg': 'ok'})
        except Exception as e:
            raise e
            return JsonResponse({'msg': str(e)})


class AssignAccountListView(ListView):
    template_name = 'member/assign_account_list.html'
    model = Account

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return render(self.request, self.template_name, {'msg': 'no'})
        return super(AssignAccountListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.dept_id = kwargs.get('dept_id', 0)
        return super(AssignAccountListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(AssignAccountListView, self).get_queryset().filter(enp__isnull=False)
        if self.dept_id:
            queryset = queryset.filter(user_dept_id=self.dept_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AssignAccountListView, self).get_context_data(**kwargs)
        context['dept_list'] = Departments.objects.all()

        if self.dept_id:
            context['select_dept'] = get_object_or_404(
                Departments, pk=self.dept_id).dept_name
        else:
            context['select_dept'] = '全部'

        return context


class DeptListView(ListView):
    template_name = 'member/dept_list.html'
    model = Departments
    paginate_by = 100

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return render(self.request, self.template_name, {'msg': 'no'})
        return super(DeptListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(DeptListView, self).get_queryset()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(DeptListView, self).get_context_data(**kwargs)
        context['roles'] = Role.objects.all()

        return context


class DeptCreateView(PassRequestMixin, CreateView):
    model = Departments

    template_name = "member/dept_create_form.html"
    form_class = DeptCreateForm
    success_url = '/member/dept'

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        return super(DeptCreateView, self).dispatch(*args, **kwargs)


class DeptUpdateView(PassRequestMixin, UpdateView):
    model = Departments

    template_name = "member/dept_update_form.html"
    form_class = DeptCreateForm
    success_url = '/member/dept'

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        return super(DeptUpdateView, self).dispatch(*args, **kwargs)

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
    success_url = '/global/success'

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
        dept_id = kwargs.get('dept_id')
        self.dept = None

        if dept_id is None:
            if not request.user.is_superuser:
                self.dept = self.request.user.user_dept
        else:
            if not request.user.is_superuser and dept_id != self.request.user.user_dept_id:
                # TODO: xx
                self.dept = self.request.user.user_dept
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
            if self.dept is not None:
                context['select_dept'] = self.dept.dept_name
                context['download_dept'] = self.dept.id
            else:
                context['select_dept'] = '全部'
                context['download_dept'] = 0
        else:
            context['dept_list'] = Departments.objects.filter(
                pk=self.request.user.user_dept.id)
            context['select_dept'] = self.dept.dept_name
            context['download_dept'] = self.dept.id
        print(context)
        return context


class MemberListDetailView(MemberListView):
    template_name = 'member/member_list_detail.html'


class MemberUpdateView(UpdateView):
    model = Member
    template_name = "member/member_add_form.html"
    form_class = MemberForm
    success_url = '/global/success'


class MemberDetailView(DetailView):
    model = Member
    template_name = "member/mobile.html"

    def get_object(self, queryset=None):
        try:
            self.kwargs[self.pk_url_kwarg] = de_base64(
                self.kwargs.get(self.pk_url_kwarg))
        except Exception as e:
            raise
        return super(MemberDetailView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        setattr(context['object'], 'qrcode',
                context.get('object').qrcode_content)
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
                mapdict=['member_id', 'dept_id', 'name', 'sex', 'birthday', 'position', 'phone', 'nation',
                         'blood_type'])

            context = {
                'import_msg': 'ok'
            }

        except IntegrityError as e:
            print(e)
            context = {
                'import_msg': '请检查Excel是否与已有数据重复'
            }
        except ValueError as e:
            print(e)
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

    column_names = ['member_id', 'dept_id', 'get_dept_name', 'name', 'sex', 'birthday', 'position', 'phone', 'nation',
                    'blood_type']
    colnames = ['员工工号', '部门id', '部门名字', '姓名',
                '性别', '生日', '职位', '电话', '民族', '血型']
    return excel.make_response_from_query_sets(
        members,
        column_names,
        'xls',
        file_name=file_name,
        colnames=colnames
    )


@login_required(login_url='/auth/login')
def index(request):
    if request.user.is_superuser:
        return redirect('/member/dept')
    else:
        return redirect('/member/member_list')


def success_view(request):
    return render(request, 'member/success.html')
