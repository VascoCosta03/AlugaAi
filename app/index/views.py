from django.contrib import messages
from .models import Categoria, Anuncio, Localizacao
from django.shortcuts import render, redirect
from django.db import IntegrityError

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

def message(request):
    return render(request, 'message.html')

def produto(request, id):
    anuncio = Anuncio.objects.get(id_anuncio=id)
    return render(request, 'produto.html', {'anuncio': anuncio})

def produtos(request):
    categorias = Categoria.objects.all().order_by('id_categoria')
    localizacoes = Localizacao.objects.all().order_by('id_localizacao')
    anuncios = Anuncio.objects.all().filter(ativo=True).order_by('id_anuncio')
    context = {
        'categorias': categorias,
        'localizacoes': localizacoes,
        'anuncios': anuncios
    }
    return render(request, 'produtos.html', context)

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

def adicionar(request):
    categorias = Categoria.objects.all().order_by('id_categoria')
    localizacoes = Localizacao.objects.all().order_by('id_localizacao')

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        localizacao_id = request.POST.get('localizacao')
        preco = request.POST.get('preco')
        descricao = request.POST.get('descricao')
        link = request.POST.get('link')

        try:
            categoria = Categoria.objects.get(id_categoria=categoria_id)
            localizacao = Localizacao.objects.get(id_localizacao=localizacao_id)

            anuncio = Anuncio(
                categoria=categoria,
                localizacao=localizacao,
                preco=preco,
                descricao=descricao,
                link=link,
                utilizador_id=1,  # Usar um valor padrão temporário para utilizador_id
                titulo="Título Temporário"  # Adicionar título temporário
            )
            anuncio.save()
            messages.success(request, 'Anúncio criado com sucesso!')
            return redirect('index')
        except Categoria.DoesNotExist:
            messages.error(request, 'Categoria não encontrada.')
        except Localizacao.DoesNotExist:
            messages.error(request, 'Localização não encontrada.')
        except IntegrityError as e:
            messages.error(request, f'Erro ao criar anúncio: {e}')
 
    context = {
        'categorias': categorias,
        'localizacoes': localizacoes
    }
    return render(request, 'anuncie.html', context)