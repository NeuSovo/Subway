# -*- coding: utf-8 -*-  

import os
from django.db import models
from django.conf import settings
from core.QR import make_pic
from core.utils import AutoOneToOneField

QR_DIR_3 = os.path.join(settings.MEDIA_ROOT, 'device_qr_3')
QR_DIR_2 = os.path.join(settings.MEDIA_ROOT, 'device_qr_2')

QR_3_NAME_TEM = '设备三级二维码_%s.png'
QR_2_NAME_TEM = '设备二级二维码_%s.png'

if not os.path.exists(QR_DIR_3):
    os.makedirs(QR_DIR_3)
if not os.path.exists(QR_DIR_2):
    os.makedirs(QR_DIR_2)


class Device(models.Model):
        # 编号 暂定自增

    status_choiced = (
        (0, '安装'),
        (1, '调试')
    )

    id = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='设备名称')
    status_id = models.IntegerField(
        default=0, choices=status_choiced, verbose_name='状态')
    profess = models.ForeignKey(to="Profess", related_name='profess',
                                on_delete=models.SET_NULL, verbose_name='专业', null=True)
    z1  = models.CharField('站点', max_length=50, null=True, blank=True)
    z2  = models.CharField('安装位置', max_length=50, null=True, blank=True)
    z3  = models.CharField('主要部件生产厂家', max_length=50, null=True, blank=True)
    z4  = models.CharField('材料名称', max_length=50, null=True, blank=True)
    z5  = models.CharField('规格型号', max_length=50, null=True, blank=True)
    z6 = models.CharField('进场时间', max_length=50, null=True, blank=True)
    z7  = models.CharField('生产厂家', max_length=50, null=True, blank=True)
    z8  = models.CharField('合格证号', max_length=50, null=True, blank=True)
    z9  = models.CharField('使用部位', max_length=50, null=True, blank=True)

    t1 = models.CharField('实验方式', max_length=50, null=True, blank=True)
    t2 = models.CharField('取样地点', max_length=50, null=True, blank=True)
    t3 = models.CharField('取样时间', max_length=50, null=True, blank=True)
    t4 = models.CharField('取样人', max_length=50, null=True, blank=True)
    t5 = models.CharField('检验项目', max_length=50, null=True, blank=True)
    t6 = models.CharField('检验日期', max_length=50, null=True, blank=True)
    t7 = models.CharField('执行标准', max_length=50, null=True, blank=True)
    t8 = models.CharField('保养内容', max_length=50, null=True, blank=True)
    t9 = models.CharField('注意事项', max_length=50, null=True, blank=True)
    t10 = models.CharField('现场验收结论', max_length=50, null=True, blank=True)

    acceptor = models.CharField(
        max_length=30, verbose_name='验收人', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        """Meta definition for Profess."""

        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        ordering = ['id']

    @property
    def qrcode(self):
        if not os.path.exists(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id)):
            self.gen_qrcode_img()
        return '/media/device_qr_3/' + QR_3_NAME_TEM % self.id

    @property
    def profess_name(self):
        return str(self.profess)

    @property
    def status_name(self):
        return self.status_choiced[self.status_id][1]

    def gen_qrcode_img(self):
        qr = make_pic([str(self.profess), self.name], '/device/detail/' + str(self.id))
        qr.save(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id), quality=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id)):
            self.gen_qrcode_img()


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
        return '/media/device_qr_2/' + QR_2_NAME_TEM % self.id

    def gen_qrcode_img(self):
        qr = make_pic(['设备信息', self.name],
                      '/device/qr2/' + str(self.id))
        qr.save(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id), quality=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id)):
            self.gen_qrcode_img()
