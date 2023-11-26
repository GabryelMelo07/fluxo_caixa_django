function carregarDashboard() {
    graficoSemanal();
    graficoMensal();
    cardDiario();
}

function graficoSemanal() {
    $.ajax({
        url: '/relatorio_movimentacoes_semanal/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var labels = [];
            var entradas = [];
            var saidas = [];

            data.soma_movimentacoes_por_dia.forEach(function (item) {
                labels.push(item.data);
                entradas.push(parseFloat(item.entrada));
                saidas.push(parseFloat(item.saida));
            });

            const grafico_semanal = document.getElementById('semanal');

            new Chart(grafico_semanal, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Entradas',
                            backgroundColor: ['#8abde2be'],
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1,
                            data: entradas,
                        },
                        {
                            label: 'Saídas',
                            backgroundColor: ['#ec202094'],
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                            data: saidas,
                        },
                    ],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        },
        error: function (error) {
            console.log(error);
        },
    });
}

function graficoMensal() {
    $.ajax({
        url: '/relatorio_movimentacoes_mensal/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var labels = [];
            var entradas = [];
            var saidas = [];

            data.soma_movimentacoes_por_mes.forEach(function (item) {
                var nome_mes = new Date(2000, item.mes - 1, 1).toLocaleString('pt-BR', { month: 'long' });

                labels.push(nome_mes);
                entradas.push(parseFloat(item.entrada));
                saidas.push(parseFloat(item.saida));
            });

            const grafico_mensal = document.getElementById('mensal');

            new Chart(grafico_mensal, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Entradas',
                            backgroundColor: ['#8abde2be'],
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1,
                            data: entradas,
                        },
                        {
                            label: 'Saídas',
                            backgroundColor: ['#ec202094'],
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                            data: saidas,
                        },
                    ],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        },
        error: function (error) {
            console.log(error);
        },
    });
}

function cardDiario() {
    var card_lucro_diario = document.getElementById('card-lucro-diario');
    var card_despesa_diario = document.getElementById('card-despesas-diario');
    var card_lucro_mensal = document.getElementById('card-lucro-mensal');
    var card_despesa_mensal = document.getElementById('card-despesas-mensal');

    $.ajax({
        url: '/relatorio_movimentacoes_diario/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            card_lucro_diario.textContent = data.lucrosHoje;
            card_despesa_diario.textContent = data.despesasHoje;
            card_lucro_mensal.textContent = data.lucroMes;
            card_despesa_mensal.textContent = data.despesasMes;
        },
        error: function (error) {
            console.log(error);
        },
    });
}