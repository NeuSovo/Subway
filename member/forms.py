from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Subway import settings
from .models import *
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class LoginForm(forms.Form):
    username = forms.CharField(
        label=u"用户名",
        error_messages={'required': u'请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class': 'validate',
                # 'placeholder': "用户名",
                'type': 'text',
            }
        ),
    )

    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'class': 'validate',
                # 'placeholder': "密码",
                'type': 'password',
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()


class DeptCreateForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['dept_name', 'dept_boss', 'dept_position', 'boos_phone']
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'input', 'placeholder': '部门名称'}),
            'dept_boss': forms.TextInput(attrs={'class': 'input', 'placeholder': '部门负责人'}),
            'dept_position': forms.TextInput(attrs={'class': 'input', 'placeholder': '职位'}),
            'boos_phone': forms.TextInput(attrs={'type': 'tel', 'placeholder': '部门电话'})
        }


class AssignAccountForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    username = forms.CharField(
        label='用户名',
        help_text='必填。150个字符或者更少。包含字母，数字和仅有的@/./+/-/_符号。',
        widget=forms.TextInput(
            attrs={'class': 'input', 'placeholder': '用户名'})
    )

    last_name = forms.CharField(
        label='姓名',
        widget=forms.TextInput(
            attrs={'class': 'input'})
    )

    position = forms.CharField(
        label='职位',
        widget=forms.TextInput(
            attrs={'class': 'input'})
    )

    password1 = forms.CharField(label='密码',
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'input',
                                        'type': 'password'}))

    password2 = forms.CharField(label='重复密码',
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'input',
                                        'type': 'password'}))

    roles = forms.ModelMultipleChoiceField(label='分配权限', queryset=Role.objects.all(), help_text='分配权限，按住Ctrl多选', required=False)

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if settings.DEBUG:
            return
        if password:
            return
            # try:
            #     password_validation.validate_password(password, self.instance)
            # except forms.ValidationError as error:
            #     self.add_error('password2', error)

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ('username', 'last_name', 'position', 'password1', 'password2',)


class AccountUpdateForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    last_name = forms.CharField(
        label='姓名',
        widget=forms.TextInput(
            attrs={'class': 'input'})
    )

    class Meta:
        model = Account
        fields = ['username', 'enp', 'last_name', 'position', 'roles']


class MemberForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class MemberUpdateForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
