from django import forms
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
                'type':'text',
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
