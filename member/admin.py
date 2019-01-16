from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _


class AccountAdmin(UserAdmin):
    filter_horizontal = ('roles',)
    readonly_fields = ('password',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('last_name', 'user_dept', 'position')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                           'roles')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'code')


admin.site.register(Role, RoleAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Permission, PermissionAdmin)
