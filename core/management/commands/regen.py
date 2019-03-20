from django.core.management.base import BaseCommand, CommandError
from device.models import Device, Profess as DeviceProfess
from material.models import Material, Profess as MaterialProfess
from member.models import Member
from safety.models import SafetyFile
from schedule.models import Schedule, Profess as ScheduleProfess
from technology.models import TechnologyFile, Profess as TechProfess
queryset = []

def gen():
    queryset.append(Device.objects.all())
    queryset.append(DeviceProfess.objects.all())
    queryset.append(Material.objects.all())
    queryset.append(MaterialProfess.objects.all())
    queryset.append(Member.objects.all())
    queryset.append(SafetyFile.objects.all())
    queryset.append(Schedule.objects.all())
    queryset.append(ScheduleProfess.objects.all())
    queryset.append(TechnologyFile.objects.all())
    queryset.append(TechProfess.objects.all())
    for i in queryset:
        for j in i:
            j.gen_qrcode_img()
    res = "change: "+ str(sum(map(len, queryset)))
    print (res)
    return res

class Command(BaseCommand):

    def add_arguments(self, parser):
        # parser.add_argument()
        pass

    def handle(self, *args, **options):
        gen()
