from django.urls import path
from . import views

urlpatterns = [
    path('', views.Cursos, name = "Cursos"),
    #"/cursos/{category_slug}/"
    path('<slug:category_slug>/',views.Cursos,name="cursos_by_category"),
    #para acceder a cursos/cualquiercategoria/cualquierproducto/
    path('<slug:category_slug>/<slug:curso_slug>/', views.curso_detail, name="curso_detail"), 
]

    