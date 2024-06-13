from django.urls import path
from .views import *

# Create your urls here.


urlpatterns = [
    path('', index, name='index'),
    path('cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('logar_usuario/', logar_usuario, name='logar_usuario'),
    path('dashboard/', dashboard, name='dashboard'),
    path('produto/', produto, name='produto'),
    path('deslogar_usuario/', deslogar_usuario, name='deslogar_usuario'),
    path('drones/', drones, name='drones'),
    path('about/', about, name='about'),
]