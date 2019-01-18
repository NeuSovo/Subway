from django.db import models

class Device(models.Model):

    profess_choiced = (
        (0, '电力变电'),
        (1, '接触网'),
        (2, '通信'),
        (3, '信号')
    )
