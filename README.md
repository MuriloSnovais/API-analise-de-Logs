# 🛡️ API de Análise de Logs (Security Log Analyzer)

Uma API RESTful desenvolvida em Python com FastAPI, projetada para receber, processar e analisar eventos de autenticação em formato JSON.

O principal objetivo do sistema é identificar possíveis comportamentos suspeitos, como múltiplas falhas de login associadas ao mesmo endereço IP, classificando os resultados de acordo com regras determinísticas.

O projeto também conta com integração opcional com a **Google Gemini API**, responsável por gerar resumos e recomendações de segurança a partir dos IPs já identificados pelo motor Python.

Desenvolvido com foco em **Cybersecurity, desenvolvimento de APIs, análise de logs e práticas DevSecOps**.

## 🚀 Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Linguagem principal |
| FastAPI | Desenvolvimento da API REST |
| Uvicorn | Servidor ASGI |
| Pydantic | Validação dos dados de entrada |
| Pytest | Testes automatizados |
| HTTPX | Testes de integração |
| Docker | Conteinerização da aplicação |
| Google Gemini API | Geração de resumos e recomendações com IA |
| python-dotenv | Gerenciamento de variáveis de ambiente |

## ⚙️ Funcionalidades

- Recebimento de eventos de autenticação em formato JSON.
- Validação de endereços IP e status de login com Pydantic.
- Identificação de IPs com 5 ou mais falhas de autenticação.
- Contabilização de tentativas falhas e bem-sucedidas.
- Cálculo da taxa de falha por endereço IP.
- Classificação de risco em níveis médio e alto.
- Ordenação dos IPs suspeitos pela quantidade de falhas.
- Integração opcional com Google Gemini API.
- Geração de resumos e recomendações de segurança com IA.
- Testes automatizados com Pytest.
- Execução em ambiente conteinerizado com Docker.

## 🧠 Motor de análise e classificação de risco

A identificação dos IPs suspeitos é realizada pelo Python, utilizando regras fixas de detecção.

A regra principal considera suspeito qualquer endereço IP que apresente **5 ou mais falhas de autenticação** durante o processamento dos eventos recebidos.

### Regras de classificação

| Condição | Classificação |
|---|---|
| 10 ou mais falhas | Alto |
| 5 ou mais falhas e nenhum login bem-sucedido | Alto |
| De 5 a 9 falhas, com pelo menos um login bem-sucedido | Médio |
| Menos de 5 falhas | Não classificado como suspeito |

A taxa de falha é calculada pela seguinte fórmula:

```python
failure_rate = failed_attempts / (failed_attempts + successful_attempts)
```

**Observação sobre os campos retornados:**

- `Try`: quantidade de tentativas que falharam, não o total de tentativas.
- `successful_attempts`: quantidade de autenticações bem-sucedidas.
- `failure_rate`: proporção de falhas em relação ao total de eventos de autenticação reconhecidos.
- `risk`: classificação de risco atribuída pelo motor Python.

A análise considera todos os eventos recebidos na requisição. Não existe, nesta versão, verificação de tentativas consecutivas ou análise por janelas temporais.

### Integração com inteligência artificial

A integração com a Google Gemini API é opcional.

O Python é responsável por processar os eventos, calcular as métricas e classificar os IPs. O Gemini recebe somente os resultados já identificados e gera um resumo explicativo e recomendações.

**A IA não contabiliza tentativas, não identifica os IPs suspeitos e não altera a classificação feita pelo Python.**

## 📁 Arquitetura do projeto

O projeto possui uma estrutura modular, separando a configuração da API, a lógica de análise, os testes e os arquivos de demonstração.

```text
/
├── app/
│   ├── __init__.py
│   ├── main.py           # Configuração do FastAPI e rotas
│   └── services.py       # Motor de análise e integração com IA
├── tests/
│   ├── __init__.py
│   └── test_main.py      # Testes automatizados com Pytest
├── data/
│   └── logs.json         # Logs fictícios para demonstração
├── Dockerfile            # Configuração do contêiner
├── requirements.txt      # Dependências do projeto
├── check_gemini.py       # Teste manual de conexão com Gemini
├── .env                  # Variáveis de ambiente (não versionado)
├── .dockerignore         # Arquivos excluídos da imagem Docker
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md
```

## 💻 Como executar o projeto

Existem duas formas de executar a aplicação: utilizando Docker ou diretamente no ambiente Python.

### Opção 1 — Docker (recomendado)

O Docker executa a aplicação em um ambiente isolado. Durante a construção da imagem, os testes automatizados também são executados pelo comando `RUN pytest`, configurado no Dockerfile.

**1. Construa a imagem Docker:**

```bash
docker build -t api-analise-logs .
```

**2. Inicie o contêiner:**

Para executar a API com a integração Gemini habilitada, forneça sua chave por meio de uma variável de ambiente:

```bash
docker run -p 8000:8000 -e GEMINI_API_KEY="SUA_CHAVE_AQUI" api-analise-logs
```

Caso não queira utilizar a integração com IA, execute sem fornecer a chave:

```bash
docker run -p 8000:8000 api-analise-logs
```

### Opção 2 — Localmente com Python

**1. Crie um ambiente virtual:**

```bash
python -m venv venv
```

**2. Ative o ambiente virtual:**

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**4. Configure a variável de ambiente para utilizar o Gemini:**

Na raiz do projeto, crie um arquivo chamado `.env`:

```env
GEMINI_API_KEY=sua_chave_aqui
```

Opcionalmente, você pode definir o modelo utilizado:

```env
GEMINI_MODEL=gemini-3.6-flash
```

O projeto utiliza `load_dotenv()` para carregar as variáveis desse arquivo automaticamente.

**5. Inicie o servidor:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em:

```text
http://localhost:8000
```

A documentação interativa do FastAPI pode ser acessada em:

```text
http://localhost:8000/docs
```

### 🔐 Proteção das credenciais

A chave da Google Gemini API deve ser mantida fora do código-fonte e dos repositórios públicos.

Certifique-se de que o arquivo `.env` esteja incluído no `.gitignore` e no `.dockerignore`.

Exemplo de conteúdo para o `.gitignore`:

```text
.env
venv/
.venv/
__pycache__/
.pytest_cache/
```

Exemplo de conteúdo para o `.dockerignore`:

```text
.env
.git/
venv/
.venv/
__pycache__/
.pytest_cache/
```

Dessa forma, as credenciais locais não são incorporadas à imagem durante o processo de build.

## 🔍 Como utilizar a API

A aplicação disponibiliza dois endpoints para análise:

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verifica se a API está online |
| POST | `/analise` | Recebe e analisa eventos de autenticação |
| POST | `/analyse` | Alias em inglês para a rota de análise |

A integração com IA pode ser habilitada utilizando o parâmetro `with_ai=true`.

### Exemplo de requisição

O exemplo abaixo envia eventos de autenticação para a rota `/analise`:

```bash
curl -X POST "http://localhost:8000/analise" \
  -H "Content-Type: application/json" \
  -d '[
    {"ip": "10.0.0.5", "login": "success"},
    {"ip": "192.168.1.15", "login": "failed"},
    {"ip": "192.168.1.15", "login": "failed"},
    {"ip": "192.168.1.15", "login": "failed"},
    {"ip": "192.168.1.15", "login": "failed"},
    {"ip": "192.168.1.15", "login": "failed"}
  ]'
```

### Exemplo de resposta sem IA

Quando a requisição é realizada sem o parâmetro `with_ai=true`, a API retorna somente os IPs classificados como suspeitos:

```json
[
  {
    "Suspect IP": "192.168.1.15",
    "Try": 5,
    "successful_attempts": 0,
    "failure_rate": 1.0,
    "risk": "high"
  }
]
```

### Exemplo de requisição com IA

Para habilitar a integração com Gemini, utilize:

```bash
curl -X POST "http://localhost:8000/analise?with_ai=true" \
  -H "Content-Type: application/json" \
  -d '[
    {"ip": "192.168.1.15", "login": "failed"},
    {"ip": "192.168.1.15", "login": "failed"},
    {"ip": "192.168.1.15", "login": "failed"},
    {"ip": "192.168.1.15", "login": "failed"},
    {"ip": "192.168.1.15", "login": "failed"}
  ]'
```

### Exemplo de resposta com IA

Quando a integração está habilitada, a API retorna a lista de suspeitos dentro de `suspects` e as informações geradas pela IA dentro de `ai`.

```json
{
  "suspects": [
    {
      "Suspect IP": "192.168.1.15",
      "Try": 5,
      "successful_attempts": 0,
      "failure_rate": 1.0,
      "risk": "high"
    }
  ],
  "ai": {
    "enabled": true,
    "summary": "Identificado um IP com cinco falhas de autenticação e 100% de taxa de insucesso.",
    "recommendations": [
      "Investigar a origem das tentativas de autenticação.",
      "Avaliar a aplicação de políticas de rate limiting.",
      "Verificar possíveis acessos indevidos às contas envolvidas."
    ]
  }
}
```

*Exemplo ilustrativo: o texto do resumo e as recomendações variam conforme a resposta gerada pelo Gemini.*

Caso existam IPs suspeitos e a chave da API não esteja configurada, o processamento feito pelo Python continua funcionando normalmente. Nesse caso, o campo `ai.enabled` será `false`, indicando que a integração não pôde ser utilizada.

## 🤖 Testando a conexão com a Google Gemini API

O projeto possui um script independente para verificar se a chave de API está configurada corretamente e se a comunicação com o serviço Gemini está funcionando.

Com o arquivo `.env` configurado, execute na raiz do projeto:

```bash
python check_gemini.py
```

O script realiza uma solicitação simples ao Gemini e espera receber uma resposta com `OK`.

Essa verificação é independente dos endpoints da API e não substitui os testes automatizados da aplicação.

## 🧪 Testes automatizados

O projeto utiliza Pytest e HTTPX para validar o funcionamento da API e as regras de detecção.

Execute os testes manualmente com:

```bash
pytest -v
```

Os testes incluem cenários como:

- Identificação de IP com seis falhas de autenticação e nenhum sucesso.
- Verificação de IPs sem quantidade suficiente de falhas.
- Validação de IP inválido.
- Funcionamento da análise sem chave da API Gemini.
- Verificação de que a IA recebe IPs previamente classificados pelo motor Python.

Os testes também são executados automaticamente durante a construção da imagem Docker, por meio do comando `RUN pytest` no Dockerfile.

## 🛤️ Jornada de desenvolvimento (Roadmap)

O projeto foi desenvolvido em etapas incrementais, com foco na construção da API, implementação das regras de análise e integração de ferramentas do ecossistema de segurança e infraestrutura.

- [x] **Fase 1 — Estrutura da API:** configuração inicial do FastAPI e validação do servidor Uvicorn.
- [x] **Fase 2 — Mock de dados:** criação de arquivos JSON simulando eventos de autenticação.
- [x] **Fase 3 — Motor de análise:** implementação da lógica de contagem e classificação com Python e `defaultdict`.
- [x] **Fase 4 — Integração:** criação dos endpoints POST para recebimento e processamento de eventos.
- [x] **Fase 5 — Validação:** implementação de schemas Pydantic para validar endereços IP e status de autenticação.
- [x] **Fase 6 — Garantia de qualidade:** criação de testes automatizados com Pytest e TestClient.
- [x] **Fase 7 — Conteinerização:** criação do Dockerfile baseado em `python:3.12-slim`, com execução dos testes durante o build.
- [x] **Fase 8 — Integração com IA:** utilização da Google Gemini API para geração de resumos e recomendações.
- [ ] **Fase 9 — Automação CI/CD:** integração planejada com GitHub Actions para validação contínua e automação de deploy.

## ⚠️ Limitações do projeto

Este projeto possui finalidade educacional e demonstrativa.

- A detecção utiliza regras fixas, não modelos de Machine Learning.
- A análise considera os eventos recebidos em cada requisição, sem janelas temporais.
- A aplicação não confirma que um endereço IP representa um ataque; ela identifica comportamentos que merecem investigação.
- As recomendações geradas pela IA devem ser avaliadas por um analista antes de qualquer ação operacional.
- Os logs utilizados para demonstração são fictícios.

## 👨‍💻 Autor

Desenvolvido por **Murilo Santana Novais**.

Projeto desenvolvido com foco em Python, Cybersecurity, análise de logs, automação e práticas DevSecOps.