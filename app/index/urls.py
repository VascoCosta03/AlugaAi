from django.urls import path
from .views import *

# Create your urls here.


urlpatterns = [
    path('', index, name='index'),
    path('cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('logar_usuario/', logar_usuario, name='logar_usuario'),
    path('dashboard/', dashboard, name='dashboard'),
    path('produto/<int:id>/', produto, name='produto'),
    path('deslogar_usuario/', deslogar_usuario, name='deslogar_usuario'),
    path('produtos/', produtos, name='produtos'),
    path('about/', about, name='about'),
    path('message/', message, name='message'),
    path('anuncie/', adicionar, name='anuncie'),
    path('adicionar/', adicionar, name='adicionar'),
]