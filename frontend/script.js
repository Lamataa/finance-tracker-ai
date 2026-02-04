const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://127.0.0.1:8000' 
    : window.location.origin + '/api';

const formDespesa = document.getElementById('form-despesa');
const listaDespesas = document.getElementById('lista-despesas');
const saldoTotal = document.getElementById('saldo-total');
const totalReceitas = document.getElementById('total-receitas');
const totalDespesas = document.getElementById('total-despesas');
const totalTransacoes = document.getElementById('total-transacoes');

let graficoCategorias = null;

document.addEventListener('DOMContentLoaded', () => {
    carregarDespesas();
    setDataHoje();
});

function setDataHoje() {
    const hoje = new Date().toISOString().split('T')[0];
    document.getElementById('data').value = hoje;
}

async function carregarDespesas() {
    try {
        const response = await fetch(`${API_URL}/despesas/`);
        const despesas = await response.json();
        renderizarDespesas(despesas);
        atualizarResumo(despesas);
        atualizarGraficoCategorias(despesas);
    } catch (error) {
        console.error('Erro ao carregar despesas:', error);
        alert('Erro ao carregar despesas. Verifique se o backend está rodando!');
    }
}

formDespesa.addEventListener('submit', async (event) => {
    event.preventDefault();

    const despesa = {
        descricao: document.getElementById('descricao').value,
        valor: parseFloat(document.getElementById('valor').value),
        tipo: document.getElementById('tipo').value,
        data: document.getElementById('data').value
    };

    try {
        const response = await fetch(`${API_URL}/despesas/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(despesa)
        });

        if (response.ok) {
            formDespesa.reset();
            setDataHoje();
            carregarDespesas();
            alert('✅ Despesa adicionada com sucesso!');
        } else {
            alert('❌ Erro ao adicionar despesa!');
        }
    } catch (error) {
        console.error('Erro ao adicionar despesa:', error);
        alert('❌ Erro de conexão. Verifique se o backend está rodando!');
    }   
});

async function deletarDespesa(id) {
    if (!confirm('Tem certeza que deseja deletar esta transação?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/despesas/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            carregarDespesas();
            alert('✅ Transação deletada!');
        }
    } catch (error) {
        console.error('Erro ao deletar:', error);
        alert('❌ Erro ao deletar!');
    }
}

function renderizarDespesas(despesas) {
    listaDespesas.innerHTML = '';
    
    if (despesas.length === 0) {
        listaDespesas.innerHTML = `
            <div class="text-center py-12 text-gray-400">
                <i class="fas fa-inbox text-6xl mb-4"></i>
                <p class="text-lg">Nenhuma transação ainda</p>
                <p class="text-sm">Adicione sua primeira transação acima!</p>
            </div>
        `;
        return;
    }
    
    despesas.sort((a, b) => new Date(b.data) - new Date(a.data));
    
    despesas.forEach(despesa => {
        const card = criarCardDespesa(despesa);
        listaDespesas.appendChild(card);
    });
}

function getIconeCategoria(categoria) {
    const icones = {
        'Transporte': '🚗',
        'Alimentação': '🍔',
        'Assinaturas': '📱',
        'Saúde': '💊',
        'Moradia': '🏠',
        'Lazer': '🎮',
        'Educação': '📚',
        'Vestuário': '👕',
        'Outros': '📦',
        'Salário': '💰',
        'Investimentos': '📈',
        'Freelance': '💻'
    };
    return icones[categoria] || '💸';
}

function criarCardDespesa(despesa) {
    const div = document.createElement('div');
    div.className = `despesa-card ${despesa.tipo} bg-white rounded-lg shadow p-4 flex items-center justify-between fade-in`;
    
    const valorFormatado = new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(despesa.valor);
    
    const dataFormatada = new Date(despesa.data + 'T00:00:00').toLocaleDateString('pt-BR');
    
    const categoriaClass = despesa.categoria.toLowerCase().replace(/\s+/g, '-').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    
    div.innerHTML = `
        <div class="flex items-center space-x-4 flex-1">
            <div class="text-3xl">
                ${getIconeCategoria(despesa.categoria)}
            </div>
            <div class="flex-1">
                <div class="flex items-center space-x-2">
                    <h3 class="font-semibold text-gray-800">${despesa.descricao}</h3>
                    <span class="categoria-badge cat-${categoriaClass}">
                        <i class="fas fa-robot mr-1"></i>
                        ${despesa.categoria}
                    </span>
                </div>
                <p class="text-sm text-gray-500">${dataFormatada}</p>
            </div>
        </div>
        <div class="flex items-center space-x-4">
            <p class="text-xl font-bold ${despesa.tipo === 'receita' ? 'text-green-600' : 'text-red-600'}">
                ${despesa.tipo === 'receita' ? '+' : '-'} ${valorFormatado}
            </p>
            <button 
                onclick="deletarDespesa(${despesa.id})"
                class="btn-delete bg-red-500 text-white px-3 py-2 rounded-lg hover:bg-red-600"
            >
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    
    return div;
}

function atualizarResumo(despesas) {
    let somaReceitas = 0;
    let somaDespesas = 0;
    
    despesas.forEach(d => {
        if (d.tipo === 'receita') {
            somaReceitas += d.valor;
        } else {
            somaDespesas += d.valor;
        }
    });
    
    const saldo = somaReceitas - somaDespesas;
    
    saldoTotal.textContent = formatarMoeda(saldo);
    totalReceitas.textContent = formatarMoeda(somaReceitas);
    totalDespesas.textContent = formatarMoeda(somaDespesas);
    totalTransacoes.textContent = despesas.length;
    
    if (saldo >= 0) {
        saldoTotal.classList.remove('text-red-600');
        saldoTotal.classList.add('text-green-600');
    } else {
        saldoTotal.classList.remove('text-green-600');
        saldoTotal.classList.add('text-red-600');
    }
}

function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

function atualizarGraficoCategorias(despesas) {
    const categorias = {};

    despesas.filter(d => d.tipo === 'despesa').forEach(d => {
        if (!categorias[d.categoria]) {
            categorias[d.categoria] = 0;
        }
        categorias[d.categoria] += d.valor;
    });
    
    const labels = Object.keys(categorias);
    const valores = Object.values(categorias);
    
    const ctx = document.getElementById('grafico-categorias');
    
    if (graficoCategorias) {
        graficoCategorias.destroy();
    }

    if (labels.length === 0) {
        return;
    }

    graficoCategorias = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: valores,
                backgroundColor: [
                    '#3b82f6',
                    '#f59e0b',
                    '#8b5cf6',
                    '#ec4899',
                    '#10b981',
                    '#6b7280'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}