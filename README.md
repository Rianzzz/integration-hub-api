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

## Como rodar

Pré-requisitos: [Poetry](https://python-poetry.org/), Python 3.14+ e Docker.

```bash
cp .env.example .env       # ajuste se quiser, os defaults já funcionam
docker compose up -d db    # sobe o Postgres
poetry install
poetry run uvicorn integration_hub.main:app --reload
```

A API sobe em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

## Testes

```bash
poetry run pytest
```

## Lint

```bash
poetry run ruff check .
```

## Status do projeto

Em desenvolvimento — construído em etapas, uma funcionalidade por commit.
