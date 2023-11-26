function carregarMovimentacoes(pagina) {
    $.ajax({
        url: '/obter_movimentacoes/',
        method: 'GET',
        data: { pagina: pagina },
        dataType: 'json',
        success: function (response) {
            $('#tabela-movimentacoes > tbody > tr').remove();
            var tableBody = $('#tabela-movimentacoes tbody');
            var movimentacoes = response.movimentacoes.movimentacoes;

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

            const paginaAnteriorElemento = document.getElementById("pagina_anterior");
            const proximaPaginaElemento = document.getElementById("proxima_pagina");
            const paginaAtualElement = document.getElementById("pagina_atual");

            paginaAtualElement.textContent = response.movimentacoes.pagina_atual;

            if (response.movimentacoes.total_paginas <= 1 || response.movimentacoes.pagina_atual == response.movimentacoes.total_paginas) {
                proximaPaginaElemento.classList.add("disabled");
            } else {
                proximaPaginaElemento.classList.remove("disabled");
            }

            if (response.movimentacoes.pagina_atual == 1) {
                paginaAnteriorElemento.classList.add("disabled");
            } else {
                paginaAnteriorElemento.classList.remove("disabled");
            }

            if ((response.movimentacoes.pagina_atual + 1) <= response.movimentacoes.total_paginas) {
                proximaPaginaElemento.onclick = function () {
                    carregarMovimentacoes(response.movimentacoes.pagina_atual + 1);
                };
            }

            if ((response.movimentacoes.pagina_atual - 1) >= 1) {
                paginaAnteriorElemento.onclick = function () {
                    carregarMovimentacoes(response.movimentacoes.pagina_atual - 1);
                };
            }
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}