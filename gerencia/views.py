from django.shortcuts import render,redirect
from .forms import NoticiaForm, CategoriaForm, NoticiaFilterForm, CategoriaFilterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Noticia, Categoria
from django.core.paginator import Paginator

# Create your views here.
@login_required
def inicio_gerencia(request):
    return render(request, 'gerencia/inicio.html')

def listagem_noticia(request):
    formularioFiltro = NoticiaFilterForm(request.GET or None)
    
    noticias = Noticia.objects.filter(usuario=request.user)  # Filtra pelo usuário logado

    if formularioFiltro.is_valid():
        if formularioFiltro.cleaned_data['titulo']:
            noticias = noticias.filter(titulo__icontains=formularioFiltro.cleaned_data['titulo'])
        if formularioFiltro.cleaned_data['data_publicacao_inicio']:
            noticias = noticias.filter(data_publicacao__gte=formularioFiltro.cleaned_data['data_publicacao_inicio'])
        if formularioFiltro.cleaned_data['data_publicacao_fim']:
            noticias = noticias.filter(data_publicacao__lte=formularioFiltro.cleaned_data['data_publicacao_fim'])
        if formularioFiltro.cleaned_data['categoria']:
            noticias = noticias.filter(categoria=formularioFiltro.cleaned_data['categoria'])
    
    contexto = {
        'noticias': noticias,
        'formularioFiltro': formularioFiltro
    }
    return render(request, 'gerencia/listagem_noticia.html',contexto)


def excluir_categoria(request, id):
    Categoria.objects.filter(id=id).delete()
    return redirect('index')

def cadastrar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)  # Cria instância sem salvar
            noticia.usuario = request.user  # Atribui o autor (usuário logado)
            noticia.save()  # Salva a notícia no banco
            return redirect('gerencia:listagem_noticia')  # Redireciona para página de sucesso
    else:
        form = NoticiaForm() 

    contexto = {'form': form}
    return render(request, 'gerencia/cadastro_noticia.html', contexto)

@login_required
def editar_noticia(request, id):
    noticia = Noticia.objects.get(id=id)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia_editada = form.save(commit=False)  # Não salva ainda
            noticia_editada.usuario = request.user 
            noticia_editada.save()  # Salva com o usuário intacto
            return redirect('gerencia:listagem_noticia')
    else:
        form = NoticiaForm(instance=noticia)
    
    contexto = {
        'form': form
    }
    return render(request, 'gerencia/cadastro_noticia.html',contexto)


def listagem_categoria(request):
    formularioFiltro = CategoriaFilterForm(request.GET or None)
    categorias = Categoria.objects.all()

    if (formularioFiltro.is_valid()):
        if (formularioFiltro.cleaned_data['nome']):
            categorias = categorias.filter(nome__icontains=formularioFiltro.cleaned_data['nome'])
    
    contexto = {
        'categorias': categorias,
        'formularioFiltro': formularioFiltro
    }
    return render(request, 'gerencia/listagem_categorias.html', contexto)

def cadastrar_categoria(request):
    if (request.method == 'POST'):
        form = CategoriaForm(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('index')
    else:
        form = CategoriaForm()

    contexto = {
        'form': form
    }
    return render(request, 'gerencia/formulario_categoria.html', contexto)

def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    if (request.method == 'POST'):
        form = CategoriaForm(request.POST, instance=categoria)
        if (form.is_valid()):
            form.save()
            return redirect('index')
    else:
        form = CategoriaForm(instance=categoria)

    contexto = {
        'form': form,
        'categoria_id': id
    }

    return render(request, 'gerencia/formulario_categoria.html', contexto)
        


def index(request):
    categoria_nome = request.GET.get('categoria')  # Obtém o parâmetro 'categoria' da URL
    page = request.GET.get('page', 1)

    # Filtra as notícias com base na categoria ou na busca

    if categoria_nome:
        categorias = Categoria.objects.filter(nome__icontains=categoria_nome)
    else:
        categorias = Categoria.objects.all()  # Pega todas as categorias para exibir no template

    paginator = Paginator(categorias.order_by("nome"), 5)

    contexto = {
        'page': paginator.get_page(page),
        'categoria_selecionada': categoria_nome,
    }
    return render(request, 'gerencia/index.html', contexto)
