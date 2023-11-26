const myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
const toastBootstrap = bootstrap.Toast.getOrCreateInstance(document.getElementById('notificacao'));

$(document).ready(function () {
    $('#movimentacao').on('submit', function (event) {
        event.preventDefault();

        var valorMovimentacao = $('#valor_movimentacao').val().replace(/\./g, '').replace(',', '.');
        var tipoMovimentacao = $('#tipo_movimentacao').val();

        if (isNaN(valorMovimentacao) || valorMovimentacao.trim() === '') {
            fecharModalEAbrirToast(`O campo "Valor" precisa ser numérico. Um valor válido é um número entre: 1 e 9999999999,99.`);
        } else if (tipoMovimentacao.trim() === 'Selecionar...') {
            fecharModalEAbrirToast(`O Tipo da movimentação precisa ser selecionado.`);
        } else {
            var formData = $(this).serialize();

            $.ajax({
                url: '/salvar_movimentacao/',
                method: 'POST',
                data: formData,
                dataType: 'json',
                success: function (response) {
                    $('#tipo_movimentacao').val('');
                    $('#valor_movimentacao').val('');
                    $('#descricao_movimentacao').val('');
                    myModal.hide();

                    if (!window.location.href.endsWith("/dashboard/"))
                        carregarMovimentacoes();
                },
                error: function (xhr, status, error) {
                    console.error(error);
                }
            });
        }
    });
});

function fecharModalEAbrirToast(message) {
    document.getElementById('mensagemToast').textContent = message;
    $('#tipo_movimentacao').val('');
    $('#valor_movimentacao').val('');
    $('#descricao_movimentacao').val('');
    myModal.hide();
    toastBootstrap.show();
}