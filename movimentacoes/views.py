import locale
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from .models import Movimentacao
from decimal import Decimal
from datetime import datetime, timedelta

def index(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def obter_movimentacoes(request):
    movimentacoes = Movimentacao.objects.all().order_by('-id')

    paginator = Paginator(movimentacoes, 14)
    numero_pagina = request.GET.get('pagina')
    pagina_movimentacoes = paginator.get_page(numero_pagina)

    data = []
    for movimentacao in pagina_movimentacoes:
        data.append({
            'id': movimentacao.pk,
            'data_hora': movimentacao.data_hora.strftime('%d/%m/%Y %H:%M'),
            'tipo': movimentacao.tipo,
            'descricao': movimentacao.descricao,
            'valor': str(movimentacao.valor)
        })

    response_data = {
        'movimentacoes': data,
        'pagina_atual': pagina_movimentacoes.number,
        'total_paginas': paginator.num_pages,
        'tem_pagina_anterior': pagina_movimentacoes.has_previous(),
        'tem_proxima_pagina': pagina_movimentacoes.has_next(),
    }

    return JsonResponse({'movimentacoes': response_data})


def obter_movimentacoes_por_data(request):
    if request.method == 'GET' and 'data_movimentacao' in request.GET:
        data_movimentacao = request.GET.get('data_movimentacao')
        data_movimentacao = datetime.strptime(data_movimentacao, '%Y-%m-%d').date()
        movimentacoes = Movimentacao.objects.filter(data_hora__date=data_movimentacao).order_by('-id')
        
        data = []
        for movimentacao in movimentacoes:
            data.append({
                'id': movimentacao.pk,
                'data_hora': movimentacao.data_hora.strftime('%d/%m/%Y %H:%M'),
                'tipo': movimentacao.tipo,
                'descricao': movimentacao.descricao,
                'valor': str(movimentacao.valor)
            })
        
        return JsonResponse({'movimentacoes': data})
    return JsonResponse({'success': False, 'error': 'Método de requisição inválido, ou data não passada.'})


def salvar_movimentacao(request):
    if request.method == 'POST':
        tipo_movimentacao = request.POST.get('tipo_movimentacao')
        valor_movimentacao = request.POST.get('valor_movimentacao')
        descricao_movimentacao = request.POST.get('descricao_movimentacao')

        valor_movimentacao_decimal = Decimal(valor_movimentacao.replace('.', '').replace(',', '.'))
        movimentacao = Movimentacao(tipo=tipo_movimentacao, valor=valor_movimentacao_decimal, descricao=descricao_movimentacao)
        movimentacao.save()

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


def relatorio_movimentacoes_semanal(request):
    if request.method == 'GET':
        data_atual = timezone.now().date()
        resultados = []

        for i in range(7):
            data_referencia = data_atual - timedelta(days=i)

            entrada_por_dia = Movimentacao.objects.filter(
                tipo='ENTRADA',
                data_hora__date=data_referencia
            ).aggregate(Sum('valor'))['valor__sum'] or 0

            saida_por_dia = Movimentacao.objects.filter(
                tipo='SAÍDA',
                data_hora__date=data_referencia
            ).aggregate(Sum('valor'))['valor__sum'] or 0

            resultados.append({
                'data': data_referencia.strftime('%d/%m/%Y'),
                'entrada': str(entrada_por_dia),
                'saida': str(saida_por_dia),
            })

        resultados.reverse()

        return JsonResponse({'soma_movimentacoes_por_dia': resultados})
    return JsonResponse({'success': False, 'error': 'Método de requisição inválido.'})


def relatorio_movimentacoes_mensal(request):
    if request.method == 'GET':
        ano_atual = timezone.now().year

        resultados = []

        for i in range(1, 13):
            entrada_por_mes = Movimentacao.objects.filter(
                tipo='ENTRADA',
                data_hora__year=ano_atual,
                data_hora__month=i
            ).aggregate(Sum('valor'))['valor__sum'] or 0

            saida_por_mes = Movimentacao.objects.filter(
                tipo='SAÍDA',
                data_hora__year=ano_atual,
                data_hora__month=i
            ).aggregate(Sum('valor'))['valor__sum'] or 0

            resultados.append({
                'mes': i,
                'entrada': str(entrada_por_mes),
                'saida': str(saida_por_mes),
            })

        return JsonResponse({'soma_movimentacoes_por_mes': resultados})
    return JsonResponse({'success': False, 'error': 'Método de requisição inválido.'})


def relatorio_movimentacoes_diario(request):
    if request.method == 'GET':
        locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')

        data_atual = timezone.now().date()

        total_entradas = Movimentacao.objects.filter(
            tipo='ENTRADA',
            data_hora__date=data_atual
        ).aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')

        total_saidas_dia = Movimentacao.objects.filter(
            tipo='SAÍDA',
            data_hora__date=data_atual
        ).aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')

        lucros_do_dia = locale.format_string('R$ %.2f', total_entradas - total_saidas_dia, grouping=True)
        total_despesas_dia = locale.format_string('R$ %.2f', total_saidas_dia, grouping=True)

        total_entradas_mes = Movimentacao.objects.filter(
            tipo='ENTRADA',
            data_hora__month=data_atual.month,
            data_hora__year=data_atual.year
        ).aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')

        total_saidas_mes = Movimentacao.objects.filter(
            tipo='SAÍDA',
            data_hora__month=data_atual.month,
            data_hora__year=data_atual.year
        ).aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')

        lucro_mes = locale.format_string('R$ %.2f', total_entradas_mes - total_saidas_mes, grouping=True)
        total_despesas_mes = locale.format_string('R$ %.2f', total_saidas_mes, grouping=True)

        response_data = {
            'lucrosHoje': lucros_do_dia,
            'despesasHoje': total_despesas_dia,
            'lucroMes': lucro_mes,
            'despesasMes': total_despesas_mes
        }

        return JsonResponse(response_data)
    return JsonResponse({'success': False, 'error': 'Método de requisição inválido.'})