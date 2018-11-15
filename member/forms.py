from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


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


class DeptCreateForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['dept_name', 'dept_boss', 'dept_position', 'boos_phone']
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'input'}),
            'dept_boss': forms.TextInput(attrs={'class': 'input'}),
            'dept_position': forms.TextInput(attrs={'class': 'input'}),
            'dept_phone': forms.TextInput(attrs={'type': 'tel'})
        }


class AssignAccountForm(UserCreationForm):
    username = forms.CharField(
        label='用户名',
        help_text='必填。150个字符或者更少。包含字母，数字和仅有的@/./+/-/_符号。',
        widget=forms.TextInput(
            attrs={'class': 'input'})
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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).first():
            raise forms.ValidationError('该账号已经分配过了')
        else:
            return username

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'last_name', 'position', 'password1', 'password2',)


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'member_avatar': forms.FileInput(attrs={'class': ''})
        }
