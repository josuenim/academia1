from django.contrib import admin
from .models import Categorias

# Register your models here.
class CategoriasAdmin(admin.ModelAdmin):
    list_display=("category_name","category_slug") 
    #Con prepopulated_fields autogenera la propiedad slug
    prepopulated_fields={'category_slug':('category_name',)}
    
admin.site.register(Categorias,CategoriasAdmin)
