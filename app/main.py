from flask import Flask, request, render_template
import pdfplumber
from transformers import pipeline
import os
import requests
from dotenv import load_dotenv
import logging

# ==========================================
# CONFIGURAÇÕES INICIAIS E CARREGAMENTO .ENV
# ==========================================

# Configura o logger para registrar uso e erros em arquivo
logging.basicConfig(
    level=logging.INFO,
    filename='usage.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Carrega variáveis do arquivo .env
load_dotenv()

# Lê a chave da API do OpenRouter (proxy para OpenAI)
openrouter_api = os.getenv("OPENROUTER_API_KEY")
if openrouter_api:
    print("Chave OpenRouter:", openrouter_api[:10], "...")
else:
    print("ATENÇÃO: OPENROUTER_API_KEY não definida!")

# Instância principal da aplicação Flask
app = Flask(__name__)

# ==========================================
# VARIÁVEIS DE USO E LIMITES
# ==========================================

# Contadores de chamadas às APIs
main_api_usage = 0
fallback_api_usage = 0
DAILY_LIMIT = 1000  # Limite arbitrário para controle de chamadas

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def extract_text_from_pdf(file):
    """Extrai o conteúdo textual de um arquivo PDF usando pdfplumber."""
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def classify_text(text):
    """
    Classifica o texto como 'Produtivo' ou 'Improdutivo'.
    Carrega o modelo Hugging Face apenas quando necessário (economia de memória).
    """
    print("Carregando modelo de classificação...")
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    labels = ["Produtivo", "Improdutivo"]
    result = classifier(text, labels)
    return result["labels"][0], result["scores"][0]

def generate_response(category, email_content):
    """
    Gera uma resposta automática com base na categoria e no conteúdo do email.
    Tenta usar o OpenRouter (GPT-3.5), com fallback para HuggingFace (GPT-2 PT-BR).
    """
    global main_api_usage, fallback_api_usage

    # Prompt enviado ao modelo de IA
    prompt = f"""Considere o seguinte email:

{email_content}

Este email foi classificado como "{category}".
Por favor, forneça uma resposta clara, profissional e adequada para este email, em português."""

    # ==========================================
    # TENTATIVA DE GERAR RESPOSTA VIA OPENROUTER
    # ==========================================

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
        main_api_usage += 1
        logging.info("OpenRouter API usada. Total de chamadas: %d", main_api_usage)
        return result_text

    # ==========================================
    # FALLBACK COM HUGGINGFACE (caso OpenRouter falhe)
    # ==========================================
    except Exception as e:
        logging.error("Erro com OpenRouter: %s", e)
        print("Erro com OpenRouter:", e)
        print("Utilizando fallback com HuggingFace...")

        try:
            print("Carregando modelo HuggingFace para fallback...")
            hf_generator = pipeline(
                "text-generation",
                model="pierreguillou/gpt2-small-portuguese"
            )
            fallback = hf_generator(
                prompt,
                max_length=150,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
                top_k=50,
                repetition_penalty=1.2,
                truncation=True
            )
            fallback_text = fallback[0]['generated_text'].strip()
            fallback_api_usage += 1
            logging.info("Fallback HuggingFace usado. Total: %d", fallback_api_usage)
            return fallback_text
        except Exception as hf_ex:
            logging.error("Erro no fallback HuggingFace: %s", hf_ex)
            print("Erro no fallback HuggingFace:", hf_ex)
            return "Erro ao gerar resposta. Tente novamente."

# ==========================================
# ROTAS FLASK
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal. Exibe o formulário e processa uploads de texto/arquivo PDF.
    Retorna o texto, classificação e resposta sugerida ao usuário.
    """
    extracted_text = ""
    classification_label = ""
    classification_score = 0.0
    ai_response = ""
    total_usage = main_api_usage + fallback_api_usage

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        input_text = request.form.get('text_input')

        # Determina origem do texto
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file and uploaded_file.filename.endswith('.txt'):
            extracted_text = uploaded_file.read().decode('utf-8')
        elif input_text:
            extracted_text = input_text.strip()

        # Se houver texto, inicia processamento
        if extracted_text:
            classification_label, classification_score = classify_text(extracted_text)
            ai_response = generate_response(classification_label, extracted_text)
            total_usage = main_api_usage + fallback_api_usage

        return render_template('index.html',
                               input_text=extracted_text,
                               classification_label=classification_label,
                               classification_score=classification_score,
                               ai_response=ai_response,
                               total_usage=total_usage,
                               daily_limit=DAILY_LIMIT)

    # GET inicial
    return render_template('index.html',
                           total_usage=total_usage,
                           daily_limit=DAILY_LIMIT)

# ==========================================
# EXECUÇÃO LOCAL (usado apenas em dev/localhost)
# ==========================================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
