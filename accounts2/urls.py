from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_1/', views.register_1, name='register_1'),

    path('pagina_catedratico/', views.pagina_catedratico, name='pagina_catedratico'),
    path('pagina_estudiante/', views.pagina_estudiante, name='pagina_estudiante'),    
    
    path('login/', views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    #path('eleccion_usuario/',views.eleccion_usuario, name='eleccion_usuario'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]
