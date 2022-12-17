from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users import models
from django.utils.translation import gettext_lazy as _
class UserAdmin(BaseUserAdmin):
    ordering=['id']
    list_display=['name' , 'email']
    list_display_links=['email']
    fieldsets = (
        (None, {
            "fields": (
                'name','email','password'
            ),
        }),
        (
            _('Permissions'), {'fields' : (
                'is_staff','is_active',"is_superuser"
            )}
        ),
        (_('Impotant Dtaes') , {'fields':('last_login',)}),
    )

    readonly_fields=['last_login']
    add_fieldsets=(
        (None , {
            'classes':('wide',) ,
            'fields':(
                'name',
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )


admin.site.register(models.User , UserAdmin)