import re
from django.conf import settings
from django.shortcuts import HttpResponse, render


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_url = request.path_info
        print (current_url)
        is_valid = False
        for valid in settings.VALID_LIST:
            if re.match(valid, current_url):
                is_valid = True
                break
        if not is_valid:
            return None

        # 当前用户的所有权限
        permission_list = request.session.get(
            'permission_list')
        print("permission_list:", permission_list)
        if not permission_list:
            return HttpResponse('当前用户无权限信息')
            # return HttpResponse('当前用户未登录！')

        # # 用户权限和当前URL进行匹配
        for item in permission_list:
            if re.match(item, current_url):
                return None
            else:
                pass
        return HttpResponse("无权限")
