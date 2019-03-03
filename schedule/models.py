# -*- coding: utf-8 -*-  

import os
from django.db import models
from django.conf import settings
from core.QR import make_pic

QR_DIR_3 = os.path.join(settings.MEDIA_ROOT, 'schedule_qr_3')
QR_DIR_2 = os.path.join(settings.MEDIA_ROOT, 'schedule_qr_2')

QR_3_NAME_TEM = '进度三级二维码_%s.png'
QR_2_NAME_TEM = '进度二级二维码_%s.png'

if not os.path.exists(QR_DIR_3):
    os.makedirs(QR_DIR_3)
if not os.path.exists(QR_DIR_2):
    os.makedirs(QR_DIR_2)
class Schedule(models.Model):
    """Model definition for Schedule."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Schedule."""

        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Schedule."""
        return self.job_name

    @property
    def undone_count(self):
        return self.design_total - self.done_count

    @property
    def qrcode(self):
        if not os.path.exists(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id)):
            self.gen_qrcode_img()
        return '/media/schedule_qr_3/' + QR_3_NAME_TEM % self.id

    @property
    def profess_name(self):
        return str(self.profess)

    def gen_qrcode_img(self):
        qr = make_pic([str(self.profess), self.job_name], '/schedule/detail/' + str(self.id))
        qr.save(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id), quality=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id)):
            self.gen_qrcode_img()
    

    # 编号 暂定自增
    id = models.AutoField(primary_key=True, verbose_name='编号')
    job_name = models.CharField(max_length=50, verbose_name='作业名称')
    unit = models.CharField(max_length=10, verbose_name='单位')
    location = models.CharField(max_length=30, verbose_name='施工地点')
    done_count = models.IntegerField(default=0, verbose_name='开累完成量')
    design_total = models.IntegerField(default=0, verbose_name='设计总量')
    last_week_plan = models.IntegerField(default=0, verbose_name='上周计划完成量')
    last_week_actual = models.IntegerField(default=0, verbose_name='上周实际完成量')
    now_week_plan = models.IntegerField(default=0, verbose_name='本周计划完成量')
    now_week_actual = models.IntegerField(default=0, verbose_name='完成总周数')
    now_week = models.IntegerField(default=1, verbose_name='当前周目')
    profess = models.ForeignKey(to="Profess", related_name='profess',
                                on_delete=models.SET_NULL, verbose_name='专业', null=True)

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

    @property
    def qrcode(self):
        if not os.path.exists(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id)):
            self.gen_qrcode_img()
        return '/media/schedule_qr_2/' + QR_2_NAME_TEM % self.id

    def gen_qrcode_img(self):
        qr = make_pic(['设备信息', self.name],
                      '/schedule/qr2/' + str(self.id))
        qr.save(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id), quality=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id)):
            self.gen_qrcode_img()
