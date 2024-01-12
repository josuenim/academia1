from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Catedratico
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

admin.site.register(Catedratico,CatedraticoAdmin)



admin.site.register(Account,AccountAdmin)

