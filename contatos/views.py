from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    # Ordena na pagina por id decrescente e filtra pra mostrar só os objetos
    # que tem o campo mostrar=True.
    contatos = Contato.objects.order_by('-id').filter(
        mostrar=True
    )

    paginator = Paginator(contatos, 5)  # Mostra 5 contatos por página
    page_number = request.GET.get('page')
    contatos = paginator.get_page(page_number)

    return render(request, 'contatos/index.html',
                  {
                      'contatos': contatos,

                  })


def detalhes_contato(request, contato_id):
    # contato = Contato.objects.get(id=contato_id) -> Invés de usar essa linha
    # usar a linha debaixo que previne erros distintos e só aparece 404
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostrar:
        raise Http404()

    return render(request, 'contatos/detalhes_contato.html',
                  {
                      'contato': contato,
                  })


def busca(request):
    # Pega o campo termo, que é o nome dado em base.html do campo de busca
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(request, messages.ERROR,
                             'Você precisa digitar alguma coisa.')
        return redirect('index')

    # Concatenando os campos nome e sobrenome para poder procurar por partes
    # Seja do nome ou do sobrenome.
    campos = Concat('nome', Value(' '), 'sobrenome')

    # Cria o campo nome_completo e atribui o valor campos
    # Filtra pra mostrar só os que tiverem mostrar=True
    # Procura por qualquer letra que tenha no nome_completo
    # Ou procura por qualquer numero que tenha em telefone.
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        mostrar=True
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )

    if int(len(contatos)) == 0:
        messages.add_message(request, messages.ERROR,
                             'Usuario nao encontrado.')
        return redirect('index')

    paginator = Paginator(contatos, 5)  # Mostra 5 contatos por página
    page_number = request.GET.get('page')
    contatos = paginator.get_page(page_number)

    return render(request, 'contatos/busca.html',
                  {
                      'contatos': contatos,

                  })
