# -*- coding: utf-8 -*-  

import os
from django.db import models
from django.conf import settings
from core.QR import make_pic

QR_DIR_3 = os.path.join(settings.MEDIA_ROOT, 'material_qr_3')
QR_DIR_2 = os.path.join(settings.MEDIA_ROOT, 'material_qr_2')

QR_3_NAME_TEM = '物资三级二维码_%s.png'
QR_2_NAME_TEM = '物资二级二维码_%s.png'

if not os.path.exists(QR_DIR_3):
    os.makedirs(QR_DIR_3)
if not os.path.exists(QR_DIR_2):
    os.makedirs(QR_DIR_2)


class Material(models.Model):

    # 编号 暂定自增
    id = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='物资名称')
    type_id = models.CharField(max_length=20, verbose_name='型号')
    profess = models.ForeignKey(to="Profess", related_name='profess',
                                on_delete=models.SET_NULL, verbose_name='专业', null=True)
    manufacturer = models.CharField(
        max_length=20, verbose_name='生产厂家', default='无')
    num = models.IntegerField(default=0, verbose_name='数量')
    unit = models.CharField(max_length=10, verbose_name='单位')

    def __str__(self):
        return self.name
    
    class Meta:
        """Meta definition for Profess."""

        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
        ordering = ['id']

    @property
    def qrcode(self):
        if not os.path.exists(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id)):
            self.gen_qrcode_img()
        return '/media/material_qr_3/' + QR_3_NAME_TEM % self.id

    @property
    def profess_name(self):
        return str(self.profess)

    def gen_qrcode_img(self):
        qr = make_pic(['专业名称：'+str(self.profess), '物资名称：' + self.name,
                       '生产厂家:'+self.manufacturer], '/material/detail/' + str(self.id))
        qr.save(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id), quality=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id)):
            self.gen_qrcode_img()


class MaterialStock(models.Model):

    operation_choices = (
        (0, 'in'),
        (1, 'out')
    )

    material = models.ForeignKey(
        Material, related_name='record', on_delete=models.CASCADE)
    count = models.IntegerField(default=0, verbose_name='数量')
    operation_date = models.DateTimeField(
        auto_now_add=True, verbose_name='操作日期')
    operation_type = models.IntegerField(
        default=0, choices=operation_choices, verbose_name='操作类型')
    create_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Profess(models.Model):
    """Model definition for Profess."""
    name = models.CharField(max_length=20)

    class Meta:
        """Meta definition for Profess."""

        verbose_name = 'Profess'
        verbose_name_plural = 'Professs'

    def __str__(self):
        """Unicode representation of Profess."""
        return self.name

    @property
    def qrcode(self):
        if not os.path.exists(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id)):
            self.gen_qrcode_img()
        return '/media/material_qr_2/' + QR_2_NAME_TEM % self.id

    def gen_qrcode_img(self):
        qr = make_pic(['物资信息', self.name],
                      '/material/qr2/' + str(self.id))
        qr.save(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id), quality=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id)):
            self.gen_qrcode_img()
