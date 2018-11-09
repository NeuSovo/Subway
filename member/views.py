from .forms import *
from .models import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator 
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView, CreateView, DeleteView

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


def reg_user_view(request):
    pass



class DeptListView(ListView):
    template_name = 'member/dept_list.html'
    model = Departments

    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        if (self.request.user.is_superuser):
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
        if (self.request.user.is_superuser):
            return render(self.request, self.template_name, {'msg': 'no'})
        return super(DeptListView, self).dispatch(*args, **kwargs) 


class DeptDeleteView(DeleteView):
    
    @method_decorator(login_required(login_url='/auth/login'))
    def dispatch(self, *args, **kwargs):
        if (self.request.user.is_superuser):
            return render(self.request, self.template_name, {'msg': 'no'})
        return super(DeptListView, self).dispatch(*args, **kwargs) 



    
