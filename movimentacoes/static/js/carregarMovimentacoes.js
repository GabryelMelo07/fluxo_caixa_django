function carregarMovimentacoes() {
    $.ajax({
        url: '/obter_movimentacoes/',
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            $('#tabela-movimentacoes > tbody > tr').remove();
            var tableBody = $('#tabela-movimentacoes tbody');
            var movimentacoes = response.movimentacoes;

            for (var i = 0; i < movimentacoes.length; i++) {
                var movimentacao = movimentacoes[i];
                tableBody.append(`
                            <tr>
                                <td class="align-middle">${movimentacao.id}</td>
                                <td class="align-middle">${movimentacao.data_hora}</td>
                                <td class="align-middle">${movimentacao.tipo}</td>
                                <td class="align-middle">${movimentacao.descricao}</td>
                                <td class="align-middle">R$ ${movimentacao.valor}</td>
                                <td class="text-center align-middle"><button type="button" class="btn btn-delete btn-sm d-flex align-items-center gap-2" onclick="deletarMovimentacao(${movimentacao.id})">Deletar<i class='bx bxs-trash'></i></button></td>
                            </tr>
                        `);
            }
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}