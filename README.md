# IA-Mail - Respostas Inteligentes

> “Do. Or do not. There is no try.”  
> – Mestre Yoda

Bem-vindo ao **IA-Mail**!  
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
- **Organização visual aprimorada**: a resposta gerada fica oculta por padrão, podendo ser visualizada com um clique.

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
│ ├── __init__.py          # Arquivo necessário para tornar 'app' um pacote Python
│ ├── templates/
│ │ └── index.html         # Template principal da aplicação
│ ├── static/
│ │ └── style.css         # Arquivo de estilos para a interface
│ └── main.py             # Código principal da aplicação Flask
├── requirements.txt       # Lista de dependências do projeto
├── Procfile               # Arquivo para configurar o deploy no Render
├── render.yaml            # Configuração de build no Render
├── runtime.txt            # Define a versão do Python usada no ambiente
├── LICENSE                # Informações de licenciamento do projeto
├── .gitignore             # Arquivos e diretórios ignorados pelo Git
├── .env (não versionado)  # Variáveis de ambiente privadas
└── README.md              # Documentação do projeto

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

## 🔮 Futuro do IA-Mail

Atualmente, IA-Mail oferece um **modelo gratuito** com limite diário de chamadas e funcionalidades otimizadas para processamento de e-mails. No entanto, estamos planejando **versões futuras** que irão expandir as capacidades da plataforma:

### 🚀 Versão Premium (Recursos Futuramente Disponíveis)
- **📷 Leitura de Imagens**: Capacidade de interpretar textos em imagens anexadas aos e-mails.
- **🤖 IA Avançada (GPT-4-turbo)**: Processamento mais rápido, respostas mais detalhadas e suporte a perguntas abertas.
- **🔄 Histórico de Consultas**: Armazenamento de respostas anteriores sem limite diário.
- **⚙️ Ajuste Personalizado**: Opções para configurar estilo e tom das respostas automáticas.
- **📡 API Profissional**: Integração direta com sistemas corporativos para otimizar fluxos de atendimento.

Essas melhorias estão em **planejamento**, e em breve disponibilizaremos **novidades sobre versões premium**. Fique atento! 🚀

## ✉️ Contato

Em caso de dúvidas ou sugestões:

- [Abrir issue no GitHub](https://github.com/FelixFreitasJr/autou-email-classifier/issues).

- ou contato direto pelo perfil no GitHub.


Atenciosamente,  
**Felix Freitas Júnior**  
*Candidato - Processo Seletivo AutoU*
