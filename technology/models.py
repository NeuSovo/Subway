from django.db import models

# Create your models here.


class TechnologyFile(models.Model):

    profess_choiced = (
        (0, '电力变电'),
        (1, '接触网'),
        (2, '通信'),
        (3, '信号')
    )
    file_type_choiced = (
        (0, '图纸会审情况'),
        (1, '技术交底'),
        (2, '作业指导书'),
        (3, '工艺工法')
    )

    # 编号 暂定自增
    id = models.AutoField(primary_key=True, verbose_name='编号')
    title = models.CharField(max_length=100, verbose_name='标题')
    profess = models.IntegerField(
        verbose_name='专业', choices=profess_choiced, default=0)
    file_type = models.IntegerField(
        verbose_name='文件类型', choices=file_type_choiced, default=0)
    file_s = models.FileField(
        verbose_name='文件', upload_to='technology_file', max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
