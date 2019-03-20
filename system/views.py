from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib import messages

from .models import *
from core.QR import make_template


def set_system_text_item(request):
    item_code = request.POST.get('item_code', None)
    if not item_code:
        return JsonResponse({'msg': 'no'})
        messages.error(request, '错误')
    item, created = Setting.objects.get_or_create(item_code=item_code)

    set_text = request.POST.get('item_value', '无')
    item.text = set_text
    item.save()
    if 'QR' in item.item_code:
        make_template()
    messages.info(request, '修改成功')
    return JsonResponse({'msg': 'ok'})


def set_system_img_item(request, item_code=None):
    item_code = request.POST.get('item_code', None)
    if not item_code:
        return JsonResponse({'msg': 'no'})
    item, created = Setting.objects.get_or_create(item_code=item_code)

    try:
        item.img = request.FILES['img']
        item.save()
        if 'QR' in item.item_code:
            make_template()
        messages.info(request, '修改成功')
    except Exception as identifier:
        messages.info(request, '修改失败')
        raise identifier
    return JsonResponse({'msg': 'ok'})


class SetQrcodeView(TemplateView):
    template_name = "system/set_qr.html"


class SetMobileView(TemplateView):
    template_name = "system/set_mobile.html"


class SetBackendView(TemplateView):
    template_name = "system/set_backend.html"


def regen(request):
    from core.management.commands.regen import gen
    d = gen()
    return JsonResponse({"msg": 'ok', "d": d})
