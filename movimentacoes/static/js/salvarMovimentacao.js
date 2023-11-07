const myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));

$(document).ready(function () {
    $('#movimentacao').on('submit', function (event) {
        event.preventDefault();
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
                carregarMovimentacoes();
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });
});