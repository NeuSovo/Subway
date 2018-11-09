from django.db import models
from django.contrib.auth.models import User


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


class UserProfile(models.Model):
    """Model definition for UserProfile."""

    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    user_dept = models.ForeignKey(Departments, on_delete=models.CASCADE)
    position = models.CharField(max_length=20)
    enp = models.CharField(max_length=155)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        """Unicode representation of UserProfile."""
        return str(self.user)

