from flask import Flask, request, render_template
import pdfplumber
from transformers import pipeline

app = Flask(__name__)

# Inicializa a pipeline de classificação zero-shot com o modelo BART
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def classify_text(text):
    candidate_labels = ["Produtivo", "Improdutivo"]
    result = classifier(text, candidate_labels)
    # Seleciona o rótulo com a maior pontuação
    classification_label = result["labels"][0]
    classification_score = result["scores"][0]
    return classification_label, classification_score

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ""
    classification_label = ""
    classification_score = 0.0

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

        return render_template('index.html',
                               input_text=extracted_text,
                               classification_label=classification_label,
                               classification_score=classification_score)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
