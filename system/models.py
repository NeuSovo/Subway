from django.db import models


# class QRSetting(models.Model):

#     class Meta:
#         verbose_name = "QRSetting"
#         verbose_name_plural = "QRSettings"

#     header_img = models.ImageField(upload_to='settings/qr', default='none')
#     template_img = models.ImageField(upload_to='settings/qr', default='none')
#     footer_img = models.ImageField(upload_to='settings/qr', default='none')


# class SystemSetting(models.Model):

#     class Meta:
#         verbose_name = 'SystemSetting'
#         verbose_name_plural = 'SystemSettings'

#     login_background = models.ImageField(
#         upload_to='settings/system',  default='none')
#     login_title = models.CharField(max_length=50, null=True)
#     header_img = models.ImageField(upload_to='settings/system', default='none')
#     footer_img = models.ImageField(upload_to='settings/system', default='none')
#     footer_text = models.CharField(max_length=50, null=True)
#     footer_comment = models.CharField(max_length=50, null=True)


# class MobileSetting(models.Model):

#     class Meta:
#         verbose_name = 'MobileSetting'
#         verbose_name_plural = 'MobileSettings'

#     login_background = models.ImageField(
#         upload_to='settings/mobile', default='none')
#     mobile_background = models.ImageField(
#         upload_to='settings/mobile', default='none')
#     header_img = models.ImageField(upload_to='settings/mobile', default='none')
#     footer_img = models.ImageField(upload_to='settings/mobile', default='none')
#     footer_text = models.CharField(max_length=50, null=True)
#     footer_comment = models.CharField(max_length=50, null=True)


class Setting(models.Model):

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.item_code

    item_code = models.CharField('设置类别', max_length=50, unique=True)
    text = models.CharField('设置类别显示', max_length=25, null=True, blank=True)
    img  = models.ImageField(upload_to='settings', default='none')
