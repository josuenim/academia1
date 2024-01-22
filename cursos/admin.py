from django.contrib import admin
from .models import Curso


# Register your models here.
class CursoAdmin(admin.ModelAdmin):
    list_display=("nombre","costo","cupo","horario","catedratico")
    prepopulated_fields={'slug':('nombre',)}
    list_filter=("category",)
admin.site.register(Curso,CursoAdmin)

