from django.conf import settings


def init_permission(user,request):
    """
    用于做用户登录成功之后，权限信息的初始化。
    :param user: 登录的用户对象
    :param request: 请求相关的对象
    :return:
    """
    if user.is_superuser:
        permissions = [{'permissions__url': '/*/'}]
    else:
        permissions = user.roles.filter(permissions__id__isnull=False).values(
            'permissions__id',    # 权限ID
            'permissions__title', # 权限名称
            'permissions__url',   # 权限URL
            'permissions__code',  # 权限CODE
        ).distinct()

    # # 获取权限信息+组+菜单，放入session，用于以后在页面上自动生成动态菜单。
    # permission_memu_list = []
    # for item in permission_list:
    #     val = {
    #         'id':item['permissions__id'],
    #         'title':item['permissions__title'],
    #         'url':item['permissions__url'],
    #         'pid':item['permissions__group_menu_id'],
    #         'menu_id':item['permissions__group__menu__id'],
    #         'menu__name':item['permissions__group__menu__name'],
    #     }
    #     permission_memu_list.append(val)
    # request.session[settings.PERMISSION_MENU_SESSION_KEY] = permission_memu_list

    # 获取权限信息，放入session，用于以后在中间件中权限进行匹配
    permission_list = []
    for permission in permissions:
        url = permission['permissions__url']
        permission_list.append(url)
    request.session['permission_list'] = permission_list

