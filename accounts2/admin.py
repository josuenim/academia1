from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Catedratico,UserProfile
from django.utils.html import format_html
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display=('email','first_name','username','last_login','date_joined','is_active')
    list_display_link=('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering= ('-date_joined',)
    list_filter=("is_account","is_catedratico","is_staff")

    filter_horizontal=() 
    fieldsets=() 

class CatedraticoAdmin(admin.ModelAdmin):
    list_display=("nombre","apellido", 'is_active')


class UserProfileAdmin(admin.ModelAdmin):
    #control que permita manejar las imagenes dentro de django admin
    def thumbnail(self,object):
        return format_html('<img src="{}" width= "30"  style="border-radios:50%;" >'.format(object.profile_picture.url))
    thumbnail.short_description='Imagen de Perfil'
    list_display = ('thumbnail', 'user','city','state','country')

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Catedratico,CatedraticoAdmin)
admin.site.register(Account,AccountAdmin)

