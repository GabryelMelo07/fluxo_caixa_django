from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Movimentacao
from django.template.loader import render_to_string

# Create your views here.
def index(request):
    return render(request, 'index.html')


def obter_movimentacoes(request):
    movimentacoes = Movimentacao.objects.all().order_by('-id')
    data = []
    for movimentacao in movimentacoes:
        data.append({
            'id': movimentacao.pk,
            'data_hora': movimentacao.data_hora.strftime('%d/%m/%Y %H:%M'),
            'tipo': movimentacao.tipo,
            'descricao': movimentacao.descricao,
            'valor': movimentacao.valor
        })
    return JsonResponse({'movimentacoes': data})


def salvar_movimentacao(request):
    if request.method == 'POST':
        tipo_movimentacao = request.POST.get('tipo_movimentacao')
        valor_movimentacao = request.POST.get('valor_movimentacao')
        descricao_movimentacao = request.POST.get('descricao_movimentacao')

        if not valor_movimentacao.replace('.', '', 1).isdigit():
            return JsonResponse({'success': False, 'error': 'Valor inserido não é válido.'})

        movimentacao = Movimentacao(tipo=tipo_movimentacao, valor=valor_movimentacao, descricao=descricao_movimentacao)
        movimentacao.save()

        # Retorna uma resposta JSON indicando sucesso
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método de requisição inválido.'})
    
    
def deletar_movimentacao(request):
    if request.method == 'POST':
        movimentacao_id = request.POST.get('id')
        try:
            movimentacao = Movimentacao.objects.get(pk=movimentacao_id)
            movimentacao.delete()
            return JsonResponse({'success': True})
        except Movimentacao.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Movimentação não encontrada.'})
    return JsonResponse({'success': False, 'error': 'Método de requisição inválido.'})