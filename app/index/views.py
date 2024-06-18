from django.contrib import messages
from .models import Categoria, Anuncio, Localizacao, Favorito, Chat, Mensagem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
import logging
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

def index(request):
    categorias_destaque = Categoria.objects.annotate(anuncio_count=Count('anuncio')).order_by('-anuncio_count')[:3]
    anuncios_destaque = Anuncio.objects.annotate(alugado_count=Count('produtoalugado')).order_by('-alugado_count')[:4]
    ids_favoritos = {}
    
    if request.user.is_authenticated:
        favoritos = Favorito.objects.filter(utilizador=request.user)
        ids_favoritos = favoritos.values_list('anuncio_id', flat=True)
        
    context = {
        'categorias_destaque': categorias_destaque,
        'anuncios_destaque': anuncios_destaque,
        'favoritos': ids_favoritos
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

@login_required(login_url='logar_usuario')
def message(request):
    chats = Chat.objects.filter(Q(utilizador1=request.user) | Q(utilizador2=request.user))

    messages = []
    messages = Mensagem.objects.filter(chat__in=chats).order_by('id_mensagem')    
    
    context = {
        'chats': chats,
        'messages': messages
    }
    return render(request, 'message.html', context)

@login_required(login_url='logar_usuario')
def adicionar(request):
    return render(request, 'message.html')

def produto(request, id):
    anuncio = Anuncio.objects.get(id_anuncio=id)
    produtos_relacionados = Anuncio.objects.filter(categoria=anuncio.categoria).exclude(id_anuncio=id).order_by('id_anuncio')[:4]
    
    context = {
        'anuncio': anuncio,
        'produtos_relacionados': produtos_relacionados
    }
    return render(request, 'produto.html', context)

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
    
    preco_id = request.GET.get('preco')
    if preco_id:
        
        if preco_id == '1':
            anuncios = anuncios.filter(preco__lte=5).order_by('id_anuncio')
            filters['preco'] = "Até 5€"
        elif preco_id == '2':
            anuncios = anuncios.filter(preco__range=(5, 20)).order_by('id_anuncio')
            filters['preco'] = "5€ a 20€"
        else:
            anuncios = anuncios.filter(preco__gte=20).order_by('id_anuncio')
            filters['preco'] = "Acima de 20€"
            
    search = request.GET.get('search')
    if search:
        anuncios = anuncios.filter(titulo__icontains=search).order_by('id_anuncio')
        filters['search'] = search
        
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

@csrf_exempt
def create_chat(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Usuário não autenticado"}, status=401)

    if request.method == "POST":
        try:
            User = get_user_model()
            user_id = request.POST.get('user_id')

            if not user_id:
                return JsonResponse({"error": "user_id não fornecido"}, status=400)

            try:
                utilizador = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "Usuário não encontrado"}, status=404)
            
            # Remover return desnecessário aqui
            chats = Chat.objects.filter(
                (Q(utilizador1=utilizador) & Q(utilizador2=request.user)) | 
                (Q(utilizador1=request.user) & Q(utilizador2=utilizador))
            )
            
            if chats.exists():
                chat = chats.first()
            else:
                chat = Chat.objects.create(utilizador1=request.user, utilizador2=utilizador)
                
            return JsonResponse({"chat_id": chat.id_chat}, status=200)
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}", exc_info=True)
            return JsonResponse({"error": "Erro interno do servidor"}, status=500)
    
    return JsonResponse({"error": "Método não permitido"}, status=405)

@csrf_exempt
def change_chat(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Usuário não autenticado"}, status=401)

    if request.method == "POST":
        try:
            chat_id = request.POST.get('chat_id')

            if not chat_id:
                return JsonResponse({"error": "chat_id não fornecido"}, status=400)
            try:
                chat = Chat.objects.get(id_chat=chat_id)
            except Chat.DoesNotExist:
                return JsonResponse({"error": "Chat não encontrado"}, status=404)
            
            mensagens = Mensagem.objects.filter(chat=chat)
            
            chat_data = {
                "id_chat": chat.id_chat,
                "utilizador1": chat.utilizador1.id,
                "utilizador2": chat.utilizador2.id,
            }
            
            if(chat.utilizador1.id == request.user.id):
                chat_data["nome"] = chat.utilizador2.first_name
            else:
                chat_data["nome"] = chat.utilizador1.first_name

            mensagens_data = []
            
            for mensagem in mensagens:
                mensagens_data.append({
                    "id_mensagem": mensagem.id_mensagem,
                    "remetente": mensagem.remetente.id,
                    "mensagem": mensagem.mensagem,
                })

            return JsonResponse({"chat": chat_data, "mensagens": mensagens_data}, status=200)
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}", exc_info=True)
            return JsonResponse({"error": "Erro interno do servidor"}, status=500)
    
    return JsonResponse({"error": "Método não permitido"}, status=405)

@csrf_exempt
def send_message(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Usuário não autenticado"}, status=401)

    if request.method == "POST":
        try:
            chat_id = request.POST.get('chat_id')
            mensagem = request.POST.get('mensagem')

            if not chat_id:
                return JsonResponse({"error": "chat_id não fornecido"}, status=400)
            if not mensagem:
                return JsonResponse({"error": "mensagem não fornecida"}, status=400)
            
            try:
                chat = Chat.objects.get(id_chat=chat_id)
            except Chat.DoesNotExist:
                return JsonResponse({"error": "Chat não encontrado"}, status=404)
            
            mensagem = Mensagem.objects.create(chat=chat, remetente=request.user, mensagem=mensagem)
            
            return JsonResponse({"id_mensagem": mensagem.id_mensagem}, status=200)
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}", exc_info=True)
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

@login_required(login_url='logar_usuario')
def adicionar(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        localizacao_id = request.POST.get('localizacao')
        preco = request.POST.get('preco')
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        link = request.POST.get('link')

        # Verificar se todos os campos necessários foram preenchidos
        if not (categoria_id and localizacao_id and preco and titulo and descricao and link):
            messages.error(request, 'Todos os campos devem ser preenchidos.')
            return render(request, 'anuncie.html', {
                'categorias': Categoria.objects.all().order_by('id_categoria'),
                'localizacoes': Localizacao.objects.all().order_by('id_localizacao')
            })

        try:
            # Verificar se a categoria e a localização existem
            categoria = Categoria.objects.get(id_categoria=categoria_id)
            localizacao = Localizacao.objects.get(id_localizacao=localizacao_id)
            utilizador = request.user

            # Criar ou obter o anúncio
            anuncio, created = Anuncio.objects.get_or_create(
                utilizador=utilizador, 
                categoria=categoria, 
                localizacao=localizacao, 
                titulo=titulo,
                preco=preco, 
                foto_url=link, 
                descricao=descricao
            )

            # Redirecionar para a página do anúncio após a criação
            return redirect('produto', id=anuncio.id_anuncio)

        except Categoria.DoesNotExist:
            messages.error(request, 'Categoria não encontrada.')
        except Localizacao.DoesNotExist:
            messages.error(request, 'Localização não encontrada.')
        except Exception as e:
            messages.error(request, f'Erro ao criar anúncio: {e}')

        return redirect('adicionar')

    else:
        # Obter todas as categorias e localizações para preencher o formulário
        categorias = Categoria.objects.all().order_by('id_categoria')
        localizacoes = Localizacao.objects.all().order_by('id_localizacao')
        context = {
            'categorias': categorias,
            'localizacoes': localizacoes
        }
        return render(request, 'anuncie.html', context)

def perfil(request):
    return render(request, 'perfil.html')
