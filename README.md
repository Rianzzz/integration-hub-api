# Integration Hub API

API que recebe dados de clientes vindos de fontes diferentes (cada uma com seu próprio formato),
normaliza tudo para um formato único e centraliza em um banco PostgreSQL.

## Arquitetura

O projeto segue uma separação em camadas, onde cada camada só conhece a camada imediatamente abaixo:

```
api/            → rotas HTTP (FastAPI). Traduz request/response, não tem regra de negócio.
services/       → regras de negócio e orquestração dos casos de uso.
repositories/   → acesso a dados (banco). A única camada que fala com o banco.
integrations/   → adapters que conversam com cada fonte externa e normalizam seus dados.
domain/         → modelos (SQLAlchemy) e schemas (Pydantic) compartilhados entre camadas.
core/           → configuração, conexão com banco, logging.
```

Fluxo típico: `api` recebe a request → chama um `service` → o `service` usa um `integration`
pra buscar os dados externos, normaliza e usa um `repository` pra persistir.

`domain/schemas.py` define os contratos Pydantic: `CustomerCreate` (dado normalizado pronto pra
persistir) e `CustomerRead` (formato de saída da API, sem o `raw_payload`).

Cada fonte externa tem um adapter em `integrations/`, que implementa `SourceAdapter`
(`fetch_raw_customers` + `normalize`). São dados simulados (sem API paga de terceiro),
mas a estrutura é a mesma que se usaria pra consumir uma API real. Cada fonte chega em um
formato diferente (Fonte A: campos em português; Fonte B: contato aninhado; Fonte C: cadastro
mínimo), e o adapter é o único lugar que conhece esse formato — pro resto do sistema, todo
cliente normalizado tem a mesma cara (`CustomerCreate`).

`CustomerSyncService` orquestra a sincronização: pra cada cliente que o adapter devolve, verifica
se já existe (por `source` + `external_id`) e decide entre criar ou atualizar. Rodar a sincronização
da mesma fonte várias vezes não duplica clientes — é *idempotente*.

## Endpoints

| Método | Rota                  | Descrição                                    |
|--------|------------------------|-----------------------------------------------|
| POST   | `/auth/token`          | Login (form: username, password) → JWT        |
| POST   | `/customers/sync`      | Sincroniza as 3 fontes (idempotente, requer login) |
| GET    | `/customers`           | Lista todos os clientes normalizados          |
| GET    | `/customers/{id}`      | Busca um cliente por id                        |
| GET    | `/health`              | Health check                                   |

## Erros e logging

Erros de domínio (`domain/exceptions.py`) são traduzidos pra respostas HTTP em um lugar só
(`main.py`), não espalhados pelos routers — ex: `CustomerNotFoundError` vira 404 automaticamente.
Qualquer erro inesperado vira 500 com uma mensagem genérica (nunca vaza detalhe interno pro
cliente) e vai pro log com o traceback completo. Logging estruturado configurado em
`core/logging.py`.

## Autenticação

`POST /customers/sync` exige autenticação (é a única rota que altera dados; leitura é pública).

```bash
curl -X POST http://localhost:8000/auth/token -d "username=admin&password=admin"
# copie o access_token da resposta

curl -X POST http://localhost:8000/customers/sync -H "Authorization: Bearer <token>"
```

Usuário/senha e a chave do JWT vêm do `.env` (`API_USERNAME`, `API_PASSWORD`, `JWT_SECRET_KEY`).

## Resiliência

`SourceAdapter` tenta buscar dados da fonte externa até 3 vezes (com espera entre tentativas)
antes de desistir, mas só para falhas de conexão — um erro de programação não é retentado às
cegas. Como isso vive na classe base, todo adapter novo ganha resiliência de graça.

## Como rodar

Pré-requisitos: [Poetry](https://python-poetry.org/), Python 3.14+ e Docker.

```bash
cp .env.example .env       # ajuste se quiser, os defaults já funcionam
docker compose up -d db    # sobe o Postgres
poetry install
poetry run uvicorn integration_hub.main:app --reload
```

A API sobe em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

## Migrations

```bash
poetry run alembic upgrade head              # aplica migrations pendentes
poetry run alembic revision --autogenerate -m "descricao"   # gera uma nova a partir dos models
```

## Testes

Os testes de repository rodam contra o Postgres real (não usam mocks nem SQLite) —
é necessário ter o `docker compose up -d db` de pé antes de rodar.

```bash
poetry run pytest
```

## Lint

```bash
poetry run ruff check .
```

## Status do projeto

Em desenvolvimento — construído em etapas, uma funcionalidade por commit.
