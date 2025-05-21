# AutoU Email Classifier

> “Do. Or do not. There is no try.”  
> – Mestre Yoda

Bem-vindo ao **AutoU Email Classifier**!  
Este projeto é uma solução digital para automatizar a leitura e classificação de emails para uma grande empresa do setor financeiro.

## Contexto do Desafio

O desafio é desenvolver uma aplicação que auxilie na gestão de um alto volume de emails, automatizando a classificação dos mesmos em duas categorias:

- **Produtivo:** Emails que requerem ação ou resposta (por exemplo, solicitações de suporte ou atualizações de casos).
- **Improdutivo:** Emails que não exigem uma ação imediata (como mensagens informativas ou de felicitações).

Nesta fase (Commit 2), já implementamos o upload e a leitura dos arquivos, seja via upload de `.txt` ou `.pdf`, ou pela inserção direta do texto.

## Funcionalidades Implementadas (Commit 2)

- **Upload de Arquivos e Input Direto:**  
  - Permite o envio de arquivos `.txt` e `.pdf`.
  - Possibilita inserir o conteúdo do email diretamente no formulário.

- **Extração de Texto:**  
  - Utiliza o `pdfplumber` para extrair texto de arquivos PDF.
  - Lê e decodifica arquivos `.txt` (UTF-8).

- **Exibição dos Resultados:**  
  - Após o processamento, o conteúdo enviado é exibido na mesma página.

## Estrutura do Projeto

autou-email-classifier/

│

├── app/

│   ├── templates/

│   │   └── index.html

│   ├── static/

│   │   └── style.css 
(opcional)

│   ├── main.py

│

├── requirements.txt

├── README.md


Esta estrutura foi definida para facilitar futuras integrações, como a classificação por AI e a geração de respostas automáticas.

## Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone <https://github.com/FelixFreitasJr/autou-email-classifier.git>
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



## Roadmap e Próximos Passos

**Fases futuras:**

- **Commit 3 – Classificação com IA:**  
  Integraremos uma pipeline de zero-shot classification utilizando, por exemplo, o modelo `facebook/bart-large-mnli` para identificar se o email é **Produtivo** ou **Improdutivo**.

- **Commit 4 – Geração de Resposta com OpenAI:**  
  Implementaremos a API do OpenAI para sugerir respostas automáticas baseadas na classificação feita.

- **Commit 5 – Integração Frontend + Backend & Refinamento:**  
  Aperfeiçoaremos a interface com Bootstrap e integraremos tudo de forma a criar uma experiência amigável para o usuário.

## Instruções de Uso e Contato

Para testar a aplicação, siga os passos descritos na seção de **Instalação e Execução**.  
Qualquer dúvida ou sugestão, entre em contato.

Atenciosamente,  
[Felix Freitas Júnior]  
[Candidato - Processo Seletivo AutoU]
