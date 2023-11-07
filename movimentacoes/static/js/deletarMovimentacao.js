const myModalConfirmarDelete = new bootstrap.Modal(document.getElementById('confirmar-deletar-movimentacao'));

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
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });
}
