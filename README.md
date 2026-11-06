
# 🛡️ API de Análise de Logs (Security Log Analyzer)

Uma API RESTful focada em segurança, desenvolvida em Python com FastAPI, projetada para processar e analisar arquivos de log em formato JSON. O principal objetivo do sistema é identificar potenciais ataques de força bruta, alertando sobre IPs com comportamentos anômalos (múltiplas falhas de login consecutivas).

Este projeto foi construído com base em práticas de **DevSecOps**, incluindo validação rigorosa de dados de entrada, testes automatizados e conteinerização.

## 🚀 Tecnologias Utilizadas

*   **Linguagem:** Python 3.12
*   **Framework Web:** FastAPI
*   **Servidor ASGI:** Uvicorn
*   **Validação de Dados:** Pydantic
*   **Testes Automatizados:** Pytest & Httpx
*   **Infraestrutura:** Docker

## 📁 Arquitetura do Projeto

O projeto segue uma estrutura de diretórios limpa e profissional, separando a lógica de negócios, os testes e os arquivos de configuração:
```text
/
├── app/
│   ├── __init__.py
│   ├── main.py           # Configuração do FastAPI e rotas
│   └── services.py       # Motor de análise e regras de negócio
├── tests/
│   ├── __init__.py
│   └── test_main.py      # Testes de integração (Pytest)
├── data/
│   └── logs.json         # Mock de dados para testes
├── Dockerfile            # Configuração do contêiner da aplicação
├── requirements.txt      # Dependências do projeto
└── README.md
```

⚙️ Como Executar o Projeto
Você pode rodar esta API de duas formas: diretamente na sua máquina usando o ambiente Python, ou de forma isolada utilizando Docker.

## Opção 1: Usando Docker (Recomendado)
O Docker garante que a API rode em um ambiente isolado, incluindo a execução automática dos testes de segurança durante o processo de build.

1. **Construa a imagem Docker** (os testes rodarão automaticamente aqui):
   
```bash
docker build -t api-analise-logs .
```
2. **Inicie o contêiner** mapeando a porta 8000:

```bash
docker run -p 8000:8000 api-analise-logs
```
## Opção 2: Localmente com Python
1. **Crie e ative um ambiente virtual**:

```python
python -m venv venv
```
```bash
source venv/bin/activate  # Linux/Mac
```
```powershell
venv\Scripts\activate     # Windows
```
2. **Instale as dependências**:

```python
pip install -r requirements.txt
```
3. **Inicie o servidor**:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
# 🎯 Como Usar a API (Exemplo Prático)
Com a API rodando, você pode enviar um log de eventos de segurança no formato JSON para a rota `/analise` (o alias `/analyse` também funciona). A regra de negócio considera suspeito qualquer IP que apresente 5 ou mais falhas de login. A contagem é determinística. A IA não decide quem é suspeito: com `?with_ai=true` ela só escreve um resumo dos IPs que a regra já marcou. Sem a variável `GEMINI_API_KEY`, a análise continua e o campo `ai.enabled` volta `false`.

Você pode usar o Swagger UI acessando http://localhost:8000/docs no seu navegador, ou usar o terminal com o comando curl:

## Requisição (POST):

```bash
curl -X 'POST' \
  'http://localhost:8000/analise' \
  -H 'Content-Type: application/json' \
  -d '[
  {"ip": "10.0.0.5", "login": "sucess"},
  {"ip": "192.168.1.15", "login": "failed"},
  {"ip": "192.168.1.15", "login": "failed"},
  {"ip": "192.168.1.15", "login": "failed"},
  {"ip": "192.168.1.15", "login": "failed"},
  {"ip": "192.168.1.15", "login": "failed"}
]'
```
**Resposta da API**:
**A API retornará apenas os IPs identificados como ameaças**.
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

O mesmo corpo, com `?with_ai=true`, devolve a lista em `suspects` e um resumo em `ai`. O modelo só recebe os IPs já marcados, não o log inteiro.

A chave fica só no ambiente, nunca no código:

```bash
export GEMINI_API_KEY="sua-chave"
```
# 🛤️ Jornada de Desenvolvimento (Roadmap)
Este projeto foi construído em etapas incrementais, focando na solidez técnica e na integração de ferramentas do ecossistema de segurança e infraestrutura:

* **Fase 1: O Esqueleto da API - Configuração inicial do FastAPI e validação do servidor Uvicorn.**

* **Fase 2: Mock de Dados - Criação de arquivos .json simulando tráfego de rede e tentativas de intrusão.**

* **Fase 3: Motor de Análise - Desenvolvimento da lógica core em Python puro (collections.Counter) para identificar anomalias nos logs.**

* **Fase 4: Integração - Criação do endpoint POST para receber payloads dinâmicos e processá-los no motor de análise.**

* **Fase 5: Camada DevSecOps - Implementação de schemas rigorosos com Pydantic para garantir que dados malformados ou injeções sejam bloqueados na entrada.**

* **Fase 6: Garantia de Qualidade - Criação da suíte de testes com Pytest e TestClient para validar falsos-positivos e falsos-negativos.**

* **Fase 7: Empacotamento - Criação do Dockerfile baseado em imagem Linux otimizada (python-slim), adicionando os testes como barreira de segurança no momento do build.**

* **Fase 8: Automação CI/CD - Integração planejada com GitHub Actions para validação contínua e automação de deploy.**
