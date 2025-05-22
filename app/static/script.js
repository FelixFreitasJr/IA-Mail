// Verifica e aplica o modo escuro ao carregar
window.onload = function () {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add("dark-mode");
        document.querySelector('.toggle-dark-btn').innerText = "Modo Claro";
    }

    // Exibe o spinner ao enviar o formulário
    document.getElementById('emailForm').addEventListener('submit', function () {
        document.getElementById('loading').style.display = 'block';
    });
};

// Alterna entre modo claro e escuro
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    var btn = document.querySelector('.toggle-dark-btn');
    btn.innerText = document.body.classList.contains("dark-mode") ? "Modo Claro" : "Modo Escuro";
    localStorage.setItem('darkMode', document.body.classList.contains("dark-mode"));
}

// Copia a resposta para a área de transferência
function copyToClipboard() {
    var responseText = document.getElementById("aiResponseText") || document.getElementById("hiddenResponse");
    if (responseText) {
        navigator.clipboard.writeText(responseText.innerText)
            .then(() => alert("Resposta copiada!"))
            .catch(err => console.error("Erro ao copiar:", err));
    }
}

// Alterna a visibilidade da resposta de e-mails improdutivos
function toggleHiddenResponse() {
    const hiddenDiv = document.getElementById("hiddenResponse");
    if (hiddenDiv) {
        hiddenDiv.style.display = hiddenDiv.style.display === "none" ? "block" : "none";
    }
}
