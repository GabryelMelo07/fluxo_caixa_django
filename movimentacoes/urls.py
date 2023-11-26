from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('obter_movimentacoes/', views.obter_movimentacoes, name='obter_movimentacoes'),
    path('obter_movimentacoes_por_data/', views.obter_movimentacoes_por_data, name='obter_movimentacoes_por_data'),
    path('relatorio_movimentacoes_diario/', views.relatorio_movimentacoes_diario, name='relatorio_movimentacoes_diario'),
    path('relatorio_movimentacoes_semanal/', views.relatorio_movimentacoes_semanal, name='relatorio_movimentacoes_semanal'),
    path('relatorio_movimentacoes_mensal/', views.relatorio_movimentacoes_mensal, name='relatorio_movimentacoes_mensal'),
    path('salvar_movimentacao/', views.salvar_movimentacao, name='salvar_movimentacao'),
    path('deletar_movimentacao/', views.deletar_movimentacao, name='deletar_movimentacao'),
]