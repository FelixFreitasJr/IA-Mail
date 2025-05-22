# AutoU Email Classifier

> “Do. Or do not. There is no try.”  
> – Mestre Yoda

Bem-vindo ao **AutoU Email Classifier**!  
Este projeto é uma solução digital para automatizar a leitura, classificação e resposta de e-mails para empresas com alto volume de comunicação.

## 🎯 Objetivo

Facilitar o atendimento ao cliente com um classificador inteligente que:

- Lê e extrai texto de e-mails (.txt, .pdf ou digitados)
- Classifica em: **Produtivo** ou **Improdutivo**
- Gera uma **resposta automática profissional**
- Mostra uso diário com limite configurável (10 chamadas)

## 🚀 Funcionalidades

### 💡 Processamento Inteligente de E-mails
- **Classificação e resposta automática** com OpenRouter (GPT-3.5-turbo)
- **Extração de Texto** via `pdfplumber`
- **Tratamento inteligente de e-mails "Improdutivos":**
  - Classificação exibida normalmente.
  - A resposta gerada fica oculta por padrão.
  - O usuário pode clicar em "Visualizar resposta sugerida" para expandir, caso deseje ver a sugestão da IA.

### 🎨 Interface e Experiência do Usuário
- **Interface responsiva e acessível** com Bootstrap
- **Modo escuro persistente** utilizando `localStorage`
- **Botão de cópia** para facilitar o compartilhamento de respostas
- **Spinner de carregamento** para indicar processamento da IA

### 🚀 Otimização e Deploy
- **Uso leve e otimizado para deploy** em Render Free Tier



## 🧱 Estrutura do Projeto

```
autou-email-classifier/
├── app/
│ ├── templates/
│ │ └── index.html
│ ├── static/
│ │ ├── style.css
│ │ └── script.js
│ └── main.py
├── requirements.txt
├── Procfile
├── render.yaml
├── .env (não versionado)
└── README.md

```

## ⚙️ Instalação Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/FelixFreitasJr/autou-email-classifier.git
   cd autou-email-classifier 

2. **Criação e Ativação do Ambiente Virtual:**

- Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

- macOS/Linux::
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instalação das Dependências:**
```bash
   pip install -r requirements.txt 
```

4. **Execução da Aplicação:**
```bash
   python app/main.py 
```

5. **Acesso à Aplicação: Abra seu navegador e acesse http://127.0.0.1:5000**


## ☁️ Deploy

Aplicação hospedada em:

🔗 [https://autou-email-classifier.onrender.com](https://autou-email-classifier.onrender.com)

> Pode levar alguns segundos para iniciar (hibernação automática).

## 💡 Como Usar

1. Faça upload de um `.pdf`, `.txt` ou cole o texto do e-mail.

2. Clique em **Gerar**.

2. Veja a **classificação** e a **resposta sugerida**.

2. Copie a resposta com 1 clique.

2. Visualize seu uso diário de chamadas.

## ✉️ Contato

Em caso de dúvidas ou sugestões:

- [Abrir issue no GitHub](https://github.com/FelixFreitasJr/autou-email-classifier/issues).

- ou contato direto pelo perfil no GitHub.


Atenciosamente,  
**Felix Freitas Júnior**  
*Candidato - Processo Seletivo AutoU*
