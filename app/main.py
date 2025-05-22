from flask import Flask, request, render_template
import pdfplumber
from transformers import pipeline
import os
import requests
from dotenv import load_dotenv
import logging

# Configura o logger para gravar em um arquivo (usage.log)
logging.basicConfig(
    level=logging.INFO,
    filename='usage.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Carrega variáveis do .env
load_dotenv()

openrouter_api = os.getenv("OPENROUTER_API_KEY")
if openrouter_api:
    print("Chave OpenRouter:", openrouter_api[:10], "...")
else:
    print("ATENÇÃO: OPENROUTER_API_KEY não definida!")


app = Flask(__name__)

# Pipeline de classificação com modelo Hugging Face
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Fallback: modelo de geração de texto em português (caso o OpenRouter falhe)
hf_generator = pipeline(
    "text-generation",
    model="pierreguillou/gpt2-small-portuguese"
)

# Variáveis globais para controle de uso
main_api_usage = 0
fallback_api_usage = 0
DAILY_LIMIT = 1000  # Valor arbitrário (ajuste conforme sua necessidade)

def extract_text_from_pdf(file):
    """Extrai o texto de um arquivo PDF."""
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def classify_text(text):
    """Classifica o texto em 'Produtivo' ou 'Improdutivo'."""
    labels = ["Produtivo", "Improdutivo"]
    result = classifier(text, labels)
    return result["labels"][0], result["scores"][0]

def generate_response(category, email_content):
    """
    Gera uma resposta automática usando o OpenRouter.
    Em caso de falha, utiliza o fallback com o modelo HuggingFace.
    Atualiza os contadores e grava o log com qual API foi utilizada.
    """
    global main_api_usage, fallback_api_usage

    prompt = f"""Considere o seguinte email:

{email_content}

Este email foi classificado como "{category}".
Por favor, forneça uma resposta clara, profissional e adequada para este email, em português."""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
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
        logging.info("OpenRouter API used. Total main API calls: %d", main_api_usage)
        return result_text
    except Exception as e:
        logging.error("Erro ao usar OpenRouter: %s", e)
        print("Erro ao usar OpenRouter:", e)
        print("Utilizando fallback com HuggingFace...")

        try:
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
            logging.info("Fallback HuggingFace used. Total fallback API calls: %d", fallback_api_usage)
            return fallback_text
        except Exception as hf_ex:
            logging.error("Erro no fallback HuggingFace: %s", hf_ex)
            print("Erro no fallback HuggingFace:", hf_ex)
            return "Erro ao gerar resposta. Tente novamente."

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ""
    classification_label = ""
    classification_score = 0.0
    ai_response = ""
    total_usage = main_api_usage + fallback_api_usage

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        input_text = request.form.get('text_input')

        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file and uploaded_file.filename.endswith('.txt'):
            extracted_text = uploaded_file.read().decode('utf-8')
        elif input_text:
            extracted_text = input_text.strip()

        if extracted_text:
            classification_label, classification_score = classify_text(extracted_text)
            ai_response = generate_response(classification_label, extracted_text)
            total_usage = main_api_usage + fallback_api_usage  # Atualiza o total após a chamada

        return render_template('index.html',
                               input_text=extracted_text,
                               classification_label=classification_label,
                               classification_score=classification_score,
                               ai_response=ai_response,
                               total_usage=total_usage,
                               daily_limit=DAILY_LIMIT)
    else:
        # Em GET, também envia os contadores para exibição
        return render_template('index.html',
                               total_usage=total_usage,
                               daily_limit=DAILY_LIMIT)

if __name__ == '__main__':
    # Utilize a variável de ambiente PORT para definir a porta, necessária para deploy
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
