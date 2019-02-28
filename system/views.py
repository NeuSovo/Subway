from django.shortcuts import render
from .models import *
from django.http import Http404, JsonResponse
from django.views.generic import TemplateView

def SetSystemTextItem(request):
    item_code = request.GET.get('item_code', None)
    if not item_code:
        return JsonResponse({'msg': 'no'})
    item, created  = Setting.objects.get_or_create(item_code=item_code)

    set_text = request.GET.get('set_text', '无')
    item.text = set_text
    item.save()
    return JsonRespnse({'msg': 'ok'})


def SetSystemImgItem(request, item_code=None):
    item_code = request.GET.get('item_code', None)
    if not item_code:
        return JsonResponse({'msg': 'no'})
    item, created  = Setting.objects.get_or_create(item_code=item_code)

    try:
        item.img =  request.FILES['img']
        item.save()
    except expression as identifier:
        raise identifier
    return JsonRespnse({'msg': 'ok'})


class SetQrcodeView(TemplateView):
    template_name = "system/set_qr.html"


class SetMobileView(TemplateView):
    template_name = "system/set_mobile.html"


class SetBackendView(TemplateView):
    template_name = "system/set_backend.html"
