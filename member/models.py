from django.db import models
from django.contrib.auth.models import User
from .utils import *

class Departments(models.Model):

    dept_name = models.CharField(max_length=120, null=False, blank=False, verbose_name='部门名称')
    dept_boss = models.CharField(max_length=30, null=False, blank=False, verbose_name='负责人')
    dept_position = models.CharField(max_length=10, null=False, blank=False, verbose_name='职务')
    boos_phone = models.CharField(max_length=11, null=False, blank=False, verbose_name='联系电话')

    class Meta:
        verbose_name = '部门'

    def __str__(self):
        """Unicode representation of Departments."""
        return self.dept_name


class AssignAccount(models.Model):
    """Model definition for AssignAccount."""

    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    user_dept = models.ForeignKey(Departments, on_delete=models.CASCADE)
    position = models.CharField(max_length=20)
    enp = models.CharField(max_length=155)

    class Meta:
        verbose_name = 'AssignAccount'
        verbose_name_plural = 'AssignAccounts'

    def __str__(self):
        """Unicode representation of AssignAccount."""
        return str(slef.user)


class Member(models.Model):
    """Model definition for Member."""

    member_id = models.CharField(max_length=11, null=False, unique=True, verbose_name='员工工号')
    member_avatar = models.ImageField(verbose_name='头像', upload_to='avatar', height_field=None, width_field=None, default='none')
    dept = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True,verbose_name='部门')
    name = models.CharField(verbose_name='姓名', max_length=50)
    sex = models.CharField(verbose_name='性别', max_length=5)
    birthday = models.CharField(verbose_name='出生年月', max_length=50)
    position = models.CharField(verbose_name='职位', max_length=50)
    phone = models.CharField(verbose_name='联系方式', max_length=11)


    class Meta:
        """Meta definition for Member."""

        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        """Unicode representation of Member."""
        return self.dept.dept_name + '/' + self.name

    @property
    def qrcode_content(self):
        return 'http://127.0.0.1:8000/member/member_detail/'+en_base64(self.id)

    @property
    def get_dept_name(self):
        return str(self.dept)
