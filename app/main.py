from flask import Flask, request, render_template
import pdfplumber
import os
import requests
from dotenv import load_dotenv

# Configuração inicial e carregamento de variáveis de ambiente
load_dotenv()
app = Flask(__name__)
openrouter_api = os.getenv("OPENROUTER_API_KEY")

# Controle de uso da API
api_usage = 0
DAILY_LIMIT = 10

# Função para extrair texto de um arquivo PDF
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

# Classificação do e-mail e geração de resposta automática
def classify_and_respond(email_content):
    global api_usage

    # Tratativa clara para limite de requisições atingido
    if api_usage >= DAILY_LIMIT:
        return ("Você atingiu o limite diário de requisições. Tente novamente amanhã.", "")

    prompt = f"""
Considere o seguinte e-mail:

{email_content}

1. Classifique como 'Produtivo' ou 'Improdutivo'.
2. Gere uma resposta clara e profissional em português.
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_api}",
                "Content-Type": "application/json"
            },
            json={"model": "openai/gpt-3.5-turbo", "messages": [
                {"role": "system", "content": "Você é um assistente de atendimento ao cliente."},
                {"role": "user", "content": prompt}
            ]}
        )
        res_json = response.json()
        full_text = res_json['choices'][0]['message']['content'].strip()
        api_usage += 1

        # Separando classificação e resposta corretamente
        classification, response = full_text.split("Resposta:", 1) if "Resposta:" in full_text else ("", full_text)
        classification = classification.replace("Classificação:", "").strip()

        return (classification, response)

    except Exception:
        return ("Erro ao gerar resposta. Tente novamente.", "")

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ""
    classification = ""
    response = ""
    error_message = ""

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        input_text = request.form.get('text_input')

        # Verifica se o arquivo enviado é compatível (não permite imagens)
        if uploaded_file and not (uploaded_file.filename.endswith('.pdf') or uploaded_file.filename.endswith('.txt')):
            error_message = "Este modelo não suporta leitura de imagens. Envie um arquivo .pdf ou .txt."
        else:
            # Define a origem do texto
            if uploaded_file and uploaded_file.filename.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file and uploaded_file.filename.endswith('.txt'):
                extracted_text = uploaded_file.read().decode('utf-8')
            elif input_text:
                extracted_text = input_text.strip()

            # Processa se houver texto válido
            if extracted_text:
                classification, response = classify_and_respond(extracted_text)

    return render_template('index.html',
                           input_text=extracted_text,
                           classification=classification,
                           response=response,
                           error_message=error_message,
                           api_usage=api_usage,
                           daily_limit=DAILY_LIMIT)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
