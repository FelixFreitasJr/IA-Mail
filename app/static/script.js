// ==========================================
// CONFIGURAÇÕES INICIAIS DA PÁGINA
// ==========================================

// Executa ações ao carregar a página
window.onload = function () {
    // Verifica se o modo escuro estava ativado na última sessão e o aplica
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add("dark-mode");
        document.querySelector('.toggle-dark-btn').innerText = "Modo Claro";
    }

    // Exibe o spinner de carregamento ao enviar o formulário
    document.getElementById('emailForm').addEventListener('submit', function () {
        document.getElementById('loading').style.display = 'block';
    });
};

// ==========================================
// FUNÇÃO: Alternar entre Modo Claro e Modo Escuro
// ==========================================

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode"); // Alterna entre os modos

    // Atualiza o texto do botão conforme o modo ativo
    var btn = document.querySelector('.toggle-dark-btn');
    if (document.body.classList.contains("dark-mode")) {
        btn.innerText = "Modo Claro";
        localStorage.setItem('darkMode', 'true'); // Salva estado no armazenamento local
    } else {
        btn.innerText = "Modo Escuro";
        localStorage.setItem('darkMode', 'false');
    }
}

// ==========================================
// FUNÇÃO: Copiar resposta gerada para a área de transferência
// ==========================================

function copyToClipboard() {
    var responseText = document.getElementById("aiResponseText");

    // Caso o texto esteja oculto, tenta buscar no bloco escondido
    if (!responseText) {
        var hiddenBox = document.getElementById("hiddenResponse");
        if (hiddenBox) {
            responseText = hiddenBox;
        }
    }

    // Se encontrou a resposta, copia para a área de transferência
    if (responseText) {
        navigator.clipboard.writeText(responseText.innerText).then(function () {
            alert("Resposta copiada para a área de transferência!");
        }).catch(function (err) {
            console.error("Erro ao copiar: ", err);
        });
    }
}

// ==========================================
// FUNÇÃO: Exibir/Ocultar resposta para emails improdutivos
// ==========================================

function toggleHiddenResponse() {
    const hiddenDiv = document.getElementById("hiddenResponse");

    // Alterna a visibilidade do elemento escondido
    if (hiddenDiv) {
        hiddenDiv.style.display = hiddenDiv.style.display === "none" ? "block" : "none";
    }
}
