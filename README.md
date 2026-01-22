# Banking System API 🏦

API RESTful para sistema bancário com suporte a Pessoas Físicas e Jurídicas, desenvolvida com Python e Flask.

## Índice

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Execução](#execução)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Endpoints da API](#endpoints-da-api)
- [Demo Online](#demo-online)
- [Testes](#testes)
- [Qualidade de Código](#qualidade-de-código)
- [Contribuindo](#contribuindo)

## Funcionalidades

- ✅ Cadastro e listagem de Pessoas Físicas
- ✅ Cadastro e listagem de Pessoas Jurídicas
- ✅ Operação de saque com limites diferenciados por tipo de pessoa
- ✅ Validação de dados com regras de negócio
- ✅ Banco de dados SQLite integrado
- ✅ Testes unitários completos
- ✅ Arquitetura MVC

## Tecnologias

- **Python 3.11+**
- **Flask** - Framework web
- **SQLite** - Banco de dados
- **Pytest** - Framework de testes
- **Pylint** - Análise de código
- **Pre-commit** - Git hooks para qualidade de código

## Instalação

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/banking_system_api.git
cd banking_system_api
```

2. **Crie e ative o ambiente virtual**
```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**

Execute o script SQL para criar as tabelas e popular com dados de exemplo:

```bash
sqlite3 storage.db < schema.sql
```

Ou execute o script Python:

```bash
python ex_case_exc.py
```

## Execução

### Desenvolvimento

```bash
python run.py
```

A API estará disponível em: `http://localhost:3000`


## Estrutura do Projeto

```
banking-system-api/
├── src/
│   ├── controllers/          # Controllers da aplicação
│   │   ├── interfaces/
│   │   ├── tests/
│   │   ├── fisica_criar_controller.py
│   │   ├── fisica_listar_controller.py
│   │   ├── juridica_criar_controller.py
│   │   └── juridica_listar_controller.py
│   ├── errors/              # Tratamento de erros
│   │   ├── error_types.py
│   │   └── error_handler.py
│   ├── main/                # Configurações principais
│   │   ├── composer/
│   │   ├── routes/
│   │   └── server/
│   ├── models/              # Modelos de dados
│   │   └── sqlite/
│   ├── validators/          # Validadores de entrada
│   │   ├── tests/
│   │   ├── fisica_criar_validator.py
│   │   └── juridica_criar_validator.py
│   └── views/               # Views e interfaces
│       ├── http_types/
│       ├── interfaces/
│       ├── tests/
│       ├── fisica_criar_views.py
│       ├── fisica_listar_views.py
│       ├── juridica_criar_views.py
│       └── juridica_listar_views.py
├── tests/                   # Testes unitários
├── .env                     # Variáveis de ambiente
├── .gitignore
├── .pylintrc               # Configuração Pylint
├── pre-commit-config.yaml  # Configuração pre-commit
├── requirements.txt        # Dependências
├── run.py                  # Arquivo principal
├── ex_case_exc.py          # Script de criação do banco
├── storage.db              # Banco de dados SQLite
└── README.md
```

## Endpoints da API

### Pessoa Física

#### Criar Pessoa Física
```http
POST /fisica
Content-Type: application/json

{
  "renda_mensal": 5000.00,
  "idade": 30,
  "nome_completo": "João Silva",
  "celular": "11987654321",
  "email": "joao.silva@email.com"
}
```

**Resposta de Sucesso (201):**
```json
{
  "data": {
    "type": "Pessoa Física",
    "count": 1,
    "attributes": {
      "id": 7,
      "renda_mensal": 5000.0,
      "idade": 30,
      "nome_completo": "João Silva",
      "celular": "11987654321",
      "email": "joao.silva@email.com",
      "categoria": "Cliente Padrão",
      "saldo": 0.0
    }
  }
}
```

#### Listar Pessoas Físicas
```http
GET /fisica
```

**Resposta de Sucesso (200):**
```json
{
  "data": {
    "type": "Pessoas Físicas",
    "count": 6,
    "attributes": [
      {
        "id": 1,
        "renda_mensal": 85000.0,
        "idade": 38,
        "nome_completo": "Harvey Specter",
        "celular": "555-1001",
        "email": "harvey.specter@pearsonhardman.com",
        "categoria": "Sócio Sênior",
        "saldo": 2500000.0
      }
    ]
  }
}
```

### Pessoa Jurídica

#### Criar Pessoa Jurídica
```http
POST /juridica
Content-Type: application/json

{
  "faturamento": 100000.00,
  "idade": 10,
  "nome_fantasia": "Empresa XYZ Ltda",
  "celular": "11987654322",
  "email_corporativo": "contato@empresa.com"
}
```

**Resposta de Sucesso (201):**
```json
{
  "data": {
    "type": "Pessoa Jurídica",
    "count": 1,
    "attributes": {
      "id": 7,
      "faturamento": 100000.0,
      "idade": 10,
      "nome_fantasia": "Empresa XYZ Ltda",
      "celular": "11987654322",
      "email_corporativo": "contato@empresa.com",
      "categoria": "Empresa Padrão",
      "saldo": 0.0
    }
  }
}
```

#### Listar Pessoas Jurídicas
```http
GET /juridica
```

**Resposta de Sucesso (200):**
```json
{
  "data": {
    "type": "Pessoas Jurídicas",
    "count": 6,
    "attributes": [
      {
        "id": 1,
        "faturamento": 50000000.0,
        "idade": 25,
        "nome_fantasia": "Pearson Hardman",
        "celular": "555-2001",
        "email_corporativo": "contato@pearsonhardman.com",
        "categoria": "Escritório de Advocacia",
        "saldo": 120000000.0
      }
    ]
  }
}
```

### Importar Collection do Postman

Para facilitar os testes, uma collection do Postman está disponível no arquivo `banking-system-api.postman_collection.json` na raiz do projeto.

**Como importar:**

1. Abra o Postman
2. Clique em **Import** no canto superior esquerdo
3. Selecione o arquivo `API Banking System.postman_collection.json`
4. A collection será importada com todos os endpoints configurados

## 🌐 Demo Online

A API está disponível online para testes:

**URL Base:** `https://banking-system-api.onrender.com`

⚠️ **Nota:** O serviço gratuito do Render pode levar alguns segundos para inicializar na primeira requisição.

**Exemplo de teste:**
```bash
curl https://banking-system-api.onrender.com/fisica
curl https://banking-system-api.onrender.com/juridica
```

## Testes

O projeto possui cobertura completa de testes unitários para todos os controllers.

### Executar todos os testes

```bash
pytest -s -v
```

### Executar com cobertura

```bash
pytest --cov=src --cov-report=html
```

O relatório HTML estará disponível em `htmlcov/index.html`

### Executar testes específicos

```bash
# Testar apenas controllers
pytest src/controllers/tests/

# Testar apenas validadores
pytest src/validators/tests/

# Testar apenas views
pytest src/views/tests/

# Executar com verbose
pytest -v

# Executar testes que falharam por último
pytest --lf
```

### Estrutura de Testes

```
tests/
├── controllers/
│   ├── test_fisica_criar_controller.py
│   ├── test_fisica_listar_controller.py
│   ├── test_juridica_criar_controller.py
│   └── test_juridica_listar_controller.py
├── validators/
│   ├── test_fisica_criar_validator.py
│   └── test_juridica_criar_validator.py
└── views/
    ├── test_fisica_criar_views.py
    ├── test_fisica_listar_views.py
    ├── test_juridica_criar_views.py
    └── test_juridica_listar_views.py
```

## Qualidade de Código

### Pylint

Análise estática de código:

```bash
# Analisar todo o código fonte
pylint src/

# Analisar arquivo específico
pylint src/controllers/fisica_criar_controller.py

# Gerar relatório
pylint src/ --output-format=text > pylint-report.txt
```

**Configuração personalizada:** `.pylintrc`

### Pre-commit

Hooks automáticos antes de cada commit garantem a qualidade do código:

```bash
# Instalar hooks
pre-commit install

# Executar manualmente em todos os arquivos
pre-commit run --all-files

# Atualizar hooks
pre-commit autoupdate
```

**Hooks configurados:**
- Trailing whitespace removal
- End of file fixer
- YAML syntax check
- Large files check
- Pylint
- Python tests

### Regras de Negócio

- ✅ **Limite de saque para Pessoa Física:** R$ 5.000,00
- ✅ **Limite de saque para Pessoa Jurídica:** R$ 50.000,00
- ✅ **Idade mínima para Pessoa Física:** 18 anos
- ✅ **Idade mínima para Pessoa Jurídica:** 0 anos
- ✅ **Renda mensal mínima:** R$ 0,00
- ✅ **Faturamento mínimo:** R$ 0,00
- ✅ **Validação de email único**
- ✅ **Validação de celular único**
- ✅ **Saldo inicial:** R$ 0,00
- ✅ **Saldo não pode ser negativo**

## Schema do Banco de Dados

### Tabela: pessoa_fisica

| Campo | Tipo | Constraints |
|-------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| renda_mensal | REAL | NOT NULL, CHECK(renda_mensal >= 0) |
| idade | INTEGER | NOT NULL, CHECK(idade >= 18) |
| nome_completo | TEXT | NOT NULL |
| celular | TEXT | NOT NULL, UNIQUE |
| email | TEXT | NOT NULL, UNIQUE |
| categoria | TEXT | NOT NULL |
| saldo | REAL | NOT NULL, DEFAULT 0.0, CHECK(saldo >= 0) |
| criado_em | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| atualizado_em | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

**Índices:**
- `idx_pessoa_fisica_email` (email)
- `idx_pessoa_fisica_celular` (celular)

**Triggers:**
- `atualizar_pessoa_fisica_timestamp` - Atualiza automaticamente `atualizado_em`

### Tabela: pessoa_juridica

| Campo | Tipo | Constraints |
|-------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| faturamento | REAL | NOT NULL, CHECK(faturamento >= 0) |
| idade | INTEGER | NOT NULL, CHECK(idade >= 0) |
| nome_fantasia | TEXT | NOT NULL |
| celular | TEXT | NOT NULL, UNIQUE |
| email_corporativo | TEXT | NOT NULL, UNIQUE |
| categoria | TEXT | NOT NULL |
| saldo | REAL | NOT NULL, DEFAULT 0.0, CHECK(saldo >= 0) |
| criado_em | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| atualizado_em | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

**Índices:**
- `idx_pessoa_juridica_email` (email_corporativo)
- `idx_pessoa_juridica_celular` (celular)

**Triggers:**
- `atualizar_pessoa_juridica_timestamp` - Atualiza automaticamente `atualizado_em`

## Contribuindo

Contribuições são bem-vindas! Por favor, siga estas diretrizes:

1. **Fork o projeto**
2. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. **Commit suas mudanças**
   ```bash
   git commit -m 'feat: Adiciona nova funcionalidade'
   ```
4. **Push para a branch**
   ```bash
   git push origin feature/nova-funcionalidade
   ```
5. **Abra um Pull Request**

## Autor

**Davi Oliveira**

- GitHub: [@davioliveira-dev](https://github.com/davioliveiraes)
- LinkedIn: [Davi Oliveira](https://www.linkedin.com/in/davioliveiraes/)

