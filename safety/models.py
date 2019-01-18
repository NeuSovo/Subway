from django.db import models


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
        verbose_name='文件', upload_to='Safety_file', max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
