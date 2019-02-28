import os
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from core.utils import *
from core.QR import make_pic

QR_DIR = os.path.join(settings.MEDIA_ROOT, 'member_qr')
QR_NAME_TEM = '员工二维码_%s.png'
if not os.path.exists(QR_DIR):
    os.makedirs(QR_DIR)

class Departments(models.Model):
    dept_name = models.CharField(
        max_length=120, null=False, blank=False, verbose_name='部门名称', unique=True)
    dept_boss = models.CharField(
        max_length=30, null=False, blank=False, verbose_name='负责人')
    dept_position = models.CharField(
        max_length=10, null=False, blank=False, verbose_name='职务')
    boos_phone = models.CharField(
        max_length=11, null=False, blank=False, verbose_name='联系电话')

    class Meta:
        verbose_name = '部门'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Departments."""
        return self.dept_name


class Account(AbstractUser):
    """Model definition for Account."""

    user_dept = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True, verbose_name='部门')
    position = models.CharField(max_length=20, null=True, blank=True, verbose_name='职位')
    enp = models.CharField(max_length=155, null=True, blank=True, verbose_name='密码')
    roles = models.ManyToManyField(verbose_name='拥有角色', to='Role', blank=True)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return str(self.username)

    @staticmethod
    def check_username_exists(username):
        return Account.objects.filter(username=username).exists()

    def has_perm2(self, perm, obj=None):
        return self.is_superuser or self.roles.filter(permissions__code=perm).exists()

    def add_role(self, role):
        self.roles.add(*list(Role.objects.filter(id__in=list(map(int,role)))))
        return True

    def has_perm2(self, perm, obj=None):
        return self.is_superuser or self.roles.filter(permissions__code=perm).exists()

    def add_role(self, role):
        self.roles.add(*list(Role.objects.filter(id__in=list(map(int,role)))))
        return True

class Role(models.Model):
    """
    角色表
        默认所有用户都有普通用户权限，既可以查看所有信息，
    """
    title = models.CharField(verbose_name='角色名称',max_length=32)

    permissions = models.ManyToManyField(verbose_name='拥有权限', to="Permission")

    def __str__(self):
        return self.title


class Permission(models.Model):
    title = models.CharField(verbose_name='权限名称',max_length=32)
    url = models.CharField(verbose_name='含正则的URL',max_length=255)
    code = models.CharField(verbose_name="权限代码",max_length=32)

    def __str__(self):
        return self.title


class Member(models.Model):
    """Model definition for Member."""

    sex_choices = (
        ('男', '男'),
        ('女', '女')
    )

    member_id = models.CharField(
        max_length=11, null=False, unique=True, verbose_name='员工工号')
    member_avatar = models.ImageField(
        verbose_name='头像', upload_to='avatar', default='none', null=True, blank=True)
    dept = models.ForeignKey(
        Departments, on_delete=models.SET_NULL, null=True, verbose_name='部门')
    name = models.CharField(verbose_name='姓名', max_length=50, null=True)
    nation = models.CharField(verbose_name='民族', default="汉", max_length=10)
    blood_type = models.CharField(verbose_name='血型', default="未知", max_length=10)
    sex = models.CharField(verbose_name='性别', max_length=5, default=" ", choices=sex_choices)
    birthday = models.CharField(verbose_name='出生年月', max_length=50, default=" ")
    position = models.CharField(verbose_name='职位', max_length=50, default=" ")
    phone = models.CharField(verbose_name='联系方式', max_length=11, default=" ")

    class Meta:
        """Meta definition for Member."""

        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        ordering = ['member_id']

    def __str__(self):
        """Unicode representation of Member."""
        return self.dept.dept_name + '/' + self.name
 
    @property
    def qrcode(self):
        return '/media/member_qr/' + QR_NAME_TEM % self.member_id

    def gen_qrcode_img(self):
        qr = make_pic([self.name, self.dept.dept_name], '/member/member_detail/'+ str(self.id))
        qr.save(os.path.join(QR_DIR, QR_NAME_TEM % self.member_id), quality=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR, QR_NAME_TEM % self.member_id)):
            self.gen_qrcode_img()

    @property
    def dept_name(self):
        return str(self.dept)



