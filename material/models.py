import os
from django.db import models
from django.conf import settings
from core.QR import make_pic

QR_DIR = os.path.join(settings.MEDIA_ROOT, 'material_qr')

class Material(models.Model):

    # 编号 暂定自增
    id = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=155, verbose_name='名称')
    type_id = models.CharField(max_length=20, verbose_name='型号')
    profess = models.ForeignKey(to="Profess", related_name='profess', on_delete=models.SET_NULL, verbose_name='专业', null=True)
    manufacturer = models.CharField(max_length=30, verbose_name='生产厂家', default='无')
    num = models.IntegerField(default=0, verbose_name='数量')
    unit = models.CharField(max_length=10, verbose_name='单位')

    def __str__(self):
        return self.name

    def gen_qrcode_img(self):
        qr = make_pic([str(self.profess), self.name, self.manufacturer], '/material/detail/'+ str(self.id))
        qr.save(os.path.join(QR_DIR, str(self.id) + '.png'), quality=100)


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


class Profess(models.Model):
    """Model definition for Profess."""
    name = models.CharField(max_length=30)

    class Meta:
        """Meta definition for Profess."""

        verbose_name = 'Profess'
        verbose_name_plural = 'Professs'

    def __str__(self):
        """Unicode representation of Profess."""
        return self.name