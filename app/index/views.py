from django.contrib import messages
from .models import Categoria, Anuncio
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    categorias_destaque = Categoria.objects.all().order_by('id_categoria')[:3]
    anuncios_destaque = Anuncio.objects.all().filter(ativo=True).order_by('id_anuncio')[:3]
    context = {
        'categorias_destaque': categorias_destaque,
        'anuncios_destaque': anuncios_destaque
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def produto(request):
    return render(request, 'produto.html')

def produtos(request):
    categorias = Categoria.objects.all().order_by('id_categoria')
    anuncios = Anuncio.objects.all().filter(ativo=True).order_by('id_anuncio')
    context = {
        'categorias': categorias,
        'anuncios': anuncios
    }
    return render(request, 'produtos.html', context)

@login_required(login_url='index')
def dashboard(request):
    return render(request, 'dashboard.html')


def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('index')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'usuarios/form_usuario.html', {"form_usuario": form_usuario})


def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('dashboard')
        else:
            messages.error(request, 'As credenciais estão incorretas')
            return redirect('index')
    else:
        form_login = AuthenticationForm()
    return render(request, 'usuarios/login.html', {"form_login": form_login})


def deslogar_usuario(request):
    logout(request)
    return redirect('index')