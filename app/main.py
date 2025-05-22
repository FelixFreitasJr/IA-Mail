from flask import Flask, request, render_template
import pdfplumber
import os
import requests
from dotenv import load_dotenv

# ==========================
# CONFIGURAÇÕES INICIAIS
# ==========================

# Carrega variáveis de ambiente do arquivo .env (se presente)
load_dotenv()

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Obtém a chave da API do OpenRouter a partir das variáveis de ambiente
openrouter_api = os.getenv("OPENROUTER_API_KEY")

# Contador de uso da API e limite diário de chamadas
api_usage = 0
DAILY_LIMIT = 10  # Define o número máximo de chamadas permitidas por dia

# ==========================
# FUNÇÕES AUXILIARES
# ==========================

def extract_text_from_pdf(file):
    """Extrai o texto de um arquivo PDF utilizando pdfplumber."""
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def classify_and_respond(email_content):
    """
    Classifica o e-mail como 'Produtivo' ou 'Improdutivo' e gera uma resposta.
    Utiliza o OpenRouter para ambas as tarefas, garantindo um fluxo automatizado.
    """
    global api_usage

    # Impede que a API seja utilizada além do limite diário
    if api_usage >= DAILY_LIMIT:
        return ("Limite diário de uso atingido.", "")

    # Define o prompt para classificação e resposta automática
    prompt = f"""
Considere o seguinte e-mail:

{email_content}

1. Classifique este e-mail como 'Produtivo' ou 'Improdutivo'.
2. Com base na classificação, forneça uma resposta clara, profissional e adequada em português.
"""

    try:
        # Realiza a chamada à API do OpenRouter para gerar a resposta
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_api}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "Você é um assistente de atendimento ao cliente."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        res_json = response.json()

        # Extrai o texto gerado pela API
        result_text = res_json['choices'][0]['message']['content'].strip()
        api_usage += 1  # Incrementa o contador de chamadas à API
        return (result_text, "")
    
    except Exception as e:
        # Retorna mensagem de erro em caso de falha na API
        return ("Erro ao gerar resposta. Tente novamente.", "")

# ==========================
# ROTAS FLASK
# ==========================

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal que lida com uploads de arquivos e entrada de texto.
    Processa o conteúdo recebido e exibe a classificação e resposta sugerida.
    """
    extracted_text = ""
    result_text = ""
    error_message = ""

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        input_text = request.form.get('text_input')

        # Determina a origem do texto (arquivo PDF, TXT ou inserção manual)
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file and uploaded_file.filename.endswith('.txt'):
            extracted_text = uploaded_file.read().decode('utf-8')
        elif input_text:
            extracted_text = input_text.strip()

        # Processa o texto se estiver disponível
        if extracted_text:
            result_text, error_message = classify_and_respond(extracted_text)

    # Renderiza a página index.html com os dados processados
    return render_template('index.html',
                           input_text=extracted_text,
                           result_text=result_text,
                           error_message=error_message,
                           api_usage=api_usage,
                           daily_limit=DAILY_LIMIT)

# ==========================
# EXECUÇÃO LOCAL DA APLICAÇÃO
# ==========================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Obtém a porta do ambiente ou usa 5000 como padrão
    app.run(host='0.0.0.0', port=port)  # Inicia o servidor Flask na porta definida
