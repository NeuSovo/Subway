from django.db import models, transaction
from django.conf import settings


class Material(models.Model):

    # 编号 暂定自增
    id = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=155, verbose_name='名称')
    type_id = models.CharField(max_length=20, verbose_name='型号')
    num = models.IntegerField(default=0, verbose_name='数量')
    unit = models.CharField(max_length=10, verbose_name='单位')

    def __str__(self):
        return self.name


class MaterialStock(models.Model):

    operation_choices = (
        (0, 'in'),
        (1, 'out')
    )

    material = models.ForeignKey(Material, related_name='record', on_delete=models.CASCADE)
    count = models.IntegerField(default=0, verbose_name='数量')
    operation_date = models.DateTimeField(auto_now_add=True, verbose_name='操作日期')
    operation_type = models.IntegerField(default=0, choices=operation_choices, verbose_name='操作类型')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
