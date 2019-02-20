from django.db import models
from core.utils import validate_file_extension


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
    profess = models.ForeignKey(to="Profess", related_name='profess', on_delete=models.SET_NULL, verbose_name='专业', null=True)
    file_type = models.IntegerField(
        verbose_name='文件类型', choices=file_type_choiced, default=0)
    file_s = models.FileField(
        verbose_name='文件', upload_to='technology/%Y/%m/%d/', null=True, blank=True, validators=[validate_file_extension])
    upload_date = models.DateTimeField(auto_now_add=True)


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
