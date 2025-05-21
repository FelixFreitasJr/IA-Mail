# AutoU Email Classifier

> “Do. Or do not. There is no try.”  
> – Mestre Yoda

Bem-vindo ao **AutoU Email Classifier**!  
Este projeto é uma solução digital para automatizar a leitura e classificação de emails para uma grande empresa do setor financeiro.

## Contexto do Desafio

O desafio é desenvolver uma aplicação que auxilie na gestão de um alto volume de emails, automatizando a classificação dos mesmos em duas categorias:

- **Produtivo:** Emails que requerem ação ou resposta (por exemplo, solicitações de suporte ou atualizações de casos).
- **Improdutivo:** Emails que não exigem uma ação imediata (como mensagens informativas ou de felicitações).

Nesta fase, já implementamos o upload e a leitura dos arquivos, seja via upload de `.txt` ou `.pdf`, ou pela inserção direta do texto.

## Funcionalidades Implementadas

- **Initial Commit:**  
  Configuração básica do repositório.

- **Commit 1 – Estrutura Inicial e Upload de Arquivos:**  
  - Estrutura do projeto definida utilizando o framework Flask, com pastas para templates, arquivos estáticos e o arquivo principal.
  - Implementação do upload de arquivos `.pdf` e `.txt` e da inserção direta de texto via formulário.
  - Renderização do conteúdo enviado na própria página.

- **Commit 2 – Extração de Texto:**  
  - Extração de texto de arquivos PDF utilizando o `pdfplumber`.
  - Leitura e decodificação de arquivos `.txt` (encoded em UTF-8).

- **Commit 3 – Classificação com IA:**  
  - Integração do modelo de classificação zero-shot (`facebook/bart-large-mnli` da Hugging Face) para classificar emails em duas categorias: **Produtivo** ou **Improdutivo**.
  - Exibição do rótulo de classificação e do score obtido, informando ao usuário a qualidade da classificação.

- **Commit Final – Geração de Resposta e Melhorias na Interface:**  
  - Integração com a API do OpenRouter (usada como proxy para OpenAI) para gerar respostas automáticas baseadas na classificação, com fallback para um modelo local (GPT-2 adaptado para português) quando a API principal não estiver disponível.
  - Implementação de um contador de uso diário e registro em log para monitorar as chamadas à API, auxiliando no controle dos limites de uso.
  - Adição de um botão "Copiar Resposta" para facilitar a transferência da resposta gerada para a área de transferência.
  - Aprimoramento da interface com:
    - Layout responsivo utilizando Bootstrap, garantindo boa experiência em dispositivos móveis e desktops.
    - Modo escuro persistente (com estado armazenado via `localStorage`), que adapta elementos como inputs, botões, área de resposta e rodapé.
    - Feedback visual com spinner de carregamento durante o processamento da requisição.


## Estrutura do Projeto

```
autou-email-classifier/
├── app/
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   └── style.css (opcional)
│   ├── main.py
│   └── requirements.txt
├── .gitignore
├── LICENSE
└── README.md

```


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

- **Funcionalidades Adicionais Recentes (Final Commit):**  
  - Geração de resposta automatizada com integração via API (usando OpenRouter como proxy para OpenAI) e fallback local (modelo GPT-2 adaptado para português).  
  - Contador de uso diário e registro de logs para monitoramento das chamadas à API.  
  - Interface responsiva com modo escuro persistente (abrangendo inputs, botões e rodapé) e funcionalidade de copiar resposta.  
  - Feedback visual aprimorado com spinner durante o processamento das solicitações.

- **Próximas Etapas:**  
  - **Integração Avançada com IA:** Explorar APIs alternativas (como OpenAI, Anthropic Claude, Cohere ou outras) para aprimorar a geração de respostas e diversificar as possibilidades.  
  - **Aprimoramento do Frontend e Backend:** Refinar as validações, otimizar os feedbacks de carregamento e aprimorar a experiência do usuário em geral.  
  - **Deploy e Demonstração:** Realizar o deploy da aplicação na nuvem e preparar um vídeo demonstrativo detalhado que evidencie todas as funcionalidades implementadas.



## Instruções de Uso e Contato

1. **Uso da Aplicação:**  
   - Após a execução, acesse a aplicação através do endereço [http://127.0.0.1:5000](http://127.0.0.1:5000).  
   - Utilize o formulário para subir um arquivo (.pdf ou .txt) ou insira manualmente o texto do email.  
   - Clique no botão **Gerar** para que o sistema classifique o email e gere uma resposta automática.  
   - Utilize o botão **Copiar Resposta** para copiar o texto gerado para a área de transferência.  
   - O contador de uso exibido informa quantas chamadas foram realizadas em relação ao limite diário configurado.

2. **Feedback e Contato:**  
   - Se tiver dúvidas, sugestões ou identificar algum problema, abra uma [issue no repositório do GitHub](https://github.com/FelixFreitasJr/autou-email-classifier/issues).  
   - Você também pode entrar em contato diretamente pelos canais indicados no repositório para suporte adicional.

Atenciosamente,  
**Felix Freitas Júnior**  
*Candidato - Processo Seletivo AutoU*

