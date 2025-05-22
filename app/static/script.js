// Verifica o dark mode ao carregar a página
window.onload = function () {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add("dark-mode");
        document.querySelector('.toggle-dark-btn').innerText = "Modo Claro";
    }
};

// Exibe o spinner ao enviar o formulário
document.getElementById('emailForm').addEventListener('submit', function () {
    document.getElementById('loading').style.display = 'block';
});

// Copia o texto da resposta para a área de transferência
function copyToClipboard() {
    var copyText = document.getElementById("aiResponseText").innerText;
    navigator.clipboard.writeText(copyText).then(function () {
        alert("Resposta copiada para a área de transferência!");
    }, function (err) {
        console.error("Erro ao copiar: ", err);
    });
}

// Alterna entre dark e light mode com persistência
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    var btn = document.querySelector('.toggle-dark-btn');
    if (document.body.classList.contains("dark-mode")) {
        btn.innerText = "Modo Claro";
        localStorage.setItem('darkMode', 'true');
    } else {
        btn.innerText = "Modo Escuro";
        localStorage.setItem('darkMode', 'false');
    }
}
