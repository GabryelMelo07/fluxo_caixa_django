const myModalConfirmarDelete = new bootstrap.Modal(document.getElementById('confirmar-deletar-movimentacao'));
const modalPesquisarPorData = document.getElementById('pesquisarPorData');

function deletarMovimentacao(idMovimentacao) {
    myModalConfirmarDelete.show();
    
    $("#voltar-exclusao-btn").on('click', function (e) {
        myModalConfirmarDelete.hide();
    });

    $("#confirmar-exclusao-btn").on('click', function (e) {
        $.ajax({
            url: '/deletar_movimentacao/',
            type: 'POST',
            data: {
                'id': idMovimentacao,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                myModalConfirmarDelete.hide();
                carregarMovimentacoes();
                if (modalPesquisarPorData.classList.contains('show')) {
                    carregarMovimentacoesPorData();
                }
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });
}
