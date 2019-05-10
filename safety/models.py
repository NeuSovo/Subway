# -*- coding: utf-8 -*-  

import os
from django.db import models
from django.conf import settings
from core.utils import validate_file_extension
from core.QR import make_pic

QR_DIR = os.path.join(settings.MEDIA_ROOT, 'safety_qr')
QR_NAME_TEM = '安全二维码_%s.png'

if not os.path.exists(QR_DIR):
    os.makedirs(QR_DIR)


class SafetyFile(models.Model):

    file_type_choiced = (
        (0, '员工岗前培训'),
        (1, '技能培训'),
        (2, '重点区域安全卡控'),
        (3, '风险源识别')
    )

    # 编号 暂定自增
    id = models.AutoField(primary_key=True, verbose_name='编号')
    title = models.CharField(max_length=20, verbose_name='标题')
    file_type = models.IntegerField(
        verbose_name='文件类型', choices=file_type_choiced, default=0)
    file_s = models.FileField(
        verbose_name='文件', upload_to='safety/%Y/%m/%d/', null=True, blank=True, validators=[validate_file_extension])
    upload_date = models.DateTimeField(auto_now_add=True)

    def gen_qrcode_img(self):
        qr = make_pic(['文件标题：'+self.title, '文件类型: '+self.file_type_choiced[self.file_type]
                       [1]], '/safety/mobile/' + str(self.id))
        qr.save(os.path.join(QR_DIR, QR_NAME_TEM % self.id), quality=100)

    @property
    def qrcode(self):
        if not os.path.exists(os.path.join(QR_DIR, QR_NAME_TEM % self.id)):
            self.gen_qrcode_img()
        return '/media/safety_qr/' + QR_NAME_TEM % self.id

    @property
    def type_display(self):
        return self.get_file_type_display()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not os.path.exists(os.path.join(QR_DIR, QR_NAME_TEM % self.id)):
            self.gen_qrcode_img()

    @property
    def file_url(self):
        if self.file_s and hasattr(self.file_s, 'url'):
            return self.file_s.url
