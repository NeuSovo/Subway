# -*- coding: utf-8 -*-  

import os
from django.db import models
from django.conf import settings
from core.utils import validate_file_extension
from core.QR import make_pic

QR_DIR_3 = os.path.join(settings.MEDIA_ROOT, 'technology_qr_3')
QR_DIR_2 = os.path.join(settings.MEDIA_ROOT, 'technology_qr_2')

QR_3_NAME_TEM = '技术三级二维码_%s.png'
QR_2_NAME_TEM = '技术二级二维码_%s.png'

if not os.path.exists(QR_DIR_3):
    os.makedirs(QR_DIR_3)
if not os.path.exists(QR_DIR_2):
    os.makedirs(QR_DIR_2)

class TechnologyFile(models.Model):

    file_type_choiced = (
        (0, '图纸会审情况'),
        (1, '技术交底'),
        (2, '作业指导书'),
        (3, '工艺工法')
    )

    # 编号 暂定自增
    id = models.AutoField(primary_key=True, verbose_name='编号')
    title = models.CharField(max_length=20, verbose_name='标题')
    profess = models.ForeignKey(to="Profess", related_name='profess', on_delete=models.SET_NULL, verbose_name='专业', null=True)
    file_type = models.IntegerField(
        verbose_name='文件类型', choices=file_type_choiced, default=0)
    file_s = models.FileField(
        verbose_name='文件', upload_to='technology/%Y/%m/%d/', null=True, blank=True, validators=[validate_file_extension])
    upload_date = models.DateTimeField(auto_now_add=True)

    @property
    def qrcode(self):
        if not os.path.exists(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id)):
            self.gen_qrcode_img()
        return '/media/technology_qr_3/' + QR_3_NAME_TEM % self.id

    def gen_qrcode_img(self):
        qr = make_pic([str(self.profess), self.file_type_choiced[self.file_type][1], self.title], '/technology/detail/'+ str(self.id))
        qr.save(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id), quality=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR_3, QR_3_NAME_TEM % self.id)):
            self.gen_qrcode_img()

    @property
    def file_url(self):
        if self.file_s and hasattr(self.file_s, 'url'):
            return self.file_s.url

    @property
    def profess_name(self):
        return str(self.profess)

    @property
    def type_display(self):
        return self.get_file_type_display()


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
        return '/media/technology_qr_2/' + QR_2_NAME_TEM % self.id

    def gen_qrcode_img(self):
        qr = make_pic(['技术信息', self.name], '/technology/qr2/'+ str(self.id))
        qr.save(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id), quality=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR_2, QR_2_NAME_TEM % self.id)):
            self.gen_qrcode_img()

