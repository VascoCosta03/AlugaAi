from django.contrib import admin
from django.urls import path
from setup.views import *
from views.usuario_views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index, name='index'),

    path('cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('logar_usuario/', logar_usuario, name='logar_usuario'),
    path('dasboard/', dasboard, name='dasboard'),
    path('deslogar_usuario/', deslogar_usuario, name='deslogar_usuario'),

    
]