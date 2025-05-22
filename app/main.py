from flask import Flask, request, render_template
import pdfplumber
import os
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Chave da API do OpenRouter
openrouter_api = os.getenv("OPENROUTER_API_KEY")

# Contador de uso da API
api_usage = 0
DAILY_LIMIT = 10  # Limite diário de chamadas

def extract_text_from_pdf(file):
    """Extrai texto de um arquivo PDF."""
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def classify_and_respond(email_content):
    """
    Classifica o e-mail como 'Produtivo' ou 'Improdutivo' e gera uma resposta.
    Utiliza o OpenRouter para ambas as tarefas.
    """
    global api_usage

    if api_usage >= DAILY_LIMIT:
        return ("Limite diário de uso atingido.", "")

    prompt = f"""
Considere o seguinte e-mail:

{email_content}

1. Classifique este e-mail como 'Produtivo' ou 'Improdutivo'.
2. Com base na classificação, forneça uma resposta clara, profissional e adequada em português.
"""

    try:
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
        result_text = res_json['choices'][0]['message']['content'].strip()
        api_usage += 1
        return (result_text, "")
    except Exception as e:
        return ("Erro ao gerar resposta. Tente novamente.", "")

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal que lida com uploads de arquivos e entrada de texto.
    """
    extracted_text = ""
    result_text = ""
    error_message = ""

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        input_text = request.form.get('text_input')

        # Determina a origem do texto
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file and uploaded_file.filename.endswith('.txt'):
            extracted_text = uploaded_file.read().decode('utf-8')
        elif input_text:
            extracted_text = input_text.strip()

        # Processa o texto se disponível
        if extracted_text:
            result_text, error_message = classify_and_respond(extracted_text)

    return render_template('index.html',
                           input_text=extracted_text,
                           result_text=result_text,
                           error_message=error_message,
                           api_usage=api_usage,
                           daily_limit=DAILY_LIMIT)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
