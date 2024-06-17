from django.contrib import messages
from .models import Categoria, Anuncio, Localizacao, Favorito
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    categorias_destaque = Categoria.objects.annotate(anuncio_count=Count('anuncio')).order_by('-anuncio_count')[:3]
    #anuncios_destaque = Anuncio.objects.all().filter(ativo=True).order_by('id_anuncio')[:3]
    anuncios_destaque = Anuncio.objects.annotate(alugado_count=Count('produtoalugado')).order_by('-alugado_count')[:3]
    context = {
        'categorias_destaque': categorias_destaque,
        'anuncios_destaque': anuncios_destaque
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

@login_required(login_url='logar_usuario')
def message(request):
    return render(request, 'message.html')

@login_required(login_url='logar_usuario')
def adicionar(request):
    return render(request, 'message.html')

def produto(request, id):
    anuncio = Anuncio.objects.get(id_anuncio=id)
    return render(request, 'produto.html', {'anuncio': anuncio})

def produtos(request):
    categorias = Categoria.objects.all().order_by('id_categoria')
    localizacoes = Localizacao.objects.all().order_by('id_localizacao')
    anuncios = Anuncio.objects.filter(ativo=True).order_by('id_anuncio')
    filters = {}
    ids_favoritos = {}
    
    if request.user.is_authenticated:
        favoritos = Favorito.objects.filter(utilizador=request.user)
        ids_favoritos = favoritos.values_list('anuncio_id', flat=True)
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        anuncios = anuncios.filter(categoria_id=categoria_id).order_by('id_anuncio')
        filters['categoria'] = str(Categoria.objects.get(id_categoria=categoria_id))
    
    localizacao_id = request.GET.get('localizacao')
    if localizacao_id:
        anuncios = anuncios.filter(localizacao_id=localizacao_id).order_by('id_anuncio')
        filters['localizacao'] = str(Localizacao.objects.get(id_localizacao=localizacao_id))
    
    estado_id = request.GET.get('estado')
    if estado_id:
        
        if estado_id == '1':
            estado = "Novo"
        elif estado_id == '2':
            estado = "Semi-novo"
        else:
            estado = "Usado"
            
        anuncios = anuncios.filter(estado=estado).order_by('id_anuncio')
        filters['estado'] = str(estado)
        
    context = {
        'categorias': categorias,
        'localizacoes': localizacoes,
        'anuncios': anuncios,
        'filtros': filters,
        'favoritos': ids_favoritos
    }
    return render(request, 'produtos.html', context)

@login_required(login_url='logar_usuario')
def favoritos(request):
    favoritos = Favorito.objects.filter(utilizador=request.user)
    return render(request, 'favoritos.html', {'favoritos': favoritos})

@csrf_exempt
def add_favorito(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Usuário não autenticado"}, status=401)
    
    if request.method == "POST":
        try:
            anuncio_id = request.POST.get('anuncio_id')
            if not anuncio_id:
                return JsonResponse({"error": "Anúncio ID não fornecido"}, status=400)
            try:
                anuncio = Anuncio.objects.get(id_anuncio=anuncio_id)
            except Anuncio.DoesNotExist:
                return JsonResponse({"error": "Anúncio não encontrado"}, status=404)
            
            utilizador = request.user

            # Verificar se o favorito já existe
            favorito, created = Favorito.objects.get_or_create(anuncio=anuncio, utilizador=utilizador)

            if created:
                return JsonResponse({"color": "text-danger"}, status=200)
            else:
                favorito.delete()
                return JsonResponse({"color": "text-muted"}, status=200)
        except Exception as e:
            logger.error(f"Erro ao adicionar aos favoritos: {e}")
            return JsonResponse({"error": "Erro interno do servidor"}, status=500)
    return JsonResponse({"error": "Método não permitido"}, status=405)

def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = CustomUserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('index')
    else:
        form_usuario = CustomUserCreationForm()
    return render(request, 'usuarios/form_usuario.html', {"form_usuario": form_usuario})


def logar_usuario(request):
    if request.method == "POST":
        form_login = AuthenticationForm(request, data=request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('index')
            else:
                messages.error(request, "Usuário ou senha inválidos")
        else:
            messages.error(request, "Usuário ou senha inválidos")
    else:
        form_login = AuthenticationForm()
    return render(request, 'usuarios/login.html', {"form_login": form_login})


def deslogar_usuario(request):
    logout(request)
    return redirect('index')