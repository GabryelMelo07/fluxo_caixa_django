from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('obter_movimentacoes/', views.obter_movimentacoes, name='obter_movimentacoes'),
    path('salvar_movimentacao/', views.salvar_movimentacao, name='salvar_movimentacao'),
    path('deletar_movimentacao/', views.deletar_movimentacao, name='deletar_movimentacao'),
]