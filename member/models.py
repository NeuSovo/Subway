from django.db import models


class Departments(models.Model):

    def __str__(self):
        return self.dept_name

    dept_name = models.CharField(max_length=120, null=False, blank=False)
    dept_boss = models.CharField(max_length=30, null=False, blank=False)
    dept_position = models.CharField(max_length=10, null=False, blank=False)
    boos_phone = models.CharField(max_length=11, null=False, blank=False)
