import os
from django.db import models
from django.conf import settings
from core.utils import validate_file_extension
from core.QR import make_pic

QR_DIR = os.path.join(settings.MEDIA_ROOT, 'safety_qr')
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
    title = models.CharField(max_length=100, verbose_name='标题')
    file_type = models.IntegerField(
        verbose_name='文件类型', choices=file_type_choiced, default=0)
    file_s = models.FileField(
        verbose_name='文件', upload_to='safety/%Y/%m/%d/', null=True, blank=True, validators=[validate_file_extension])
    upload_date = models.DateTimeField(auto_now_add=True)


    def gen_qrcode_img(self):
        qr = make_pic([self.title, self.file_type_choiced[self.file_type][1]], '/safety/detail/'+ str(self.id))
        qr.save(os.path.join(QR_DIR, str(self.id) + '.png'), quality=100)
