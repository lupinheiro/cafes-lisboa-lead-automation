# Cafés Lisboa — Lead Prospecting & Outreach Automation

Sistema de automação de prospeção de clientes B2B (pastelarias, cafés, bares e
restaurantes) para a marca de café **Cafés Lisboa**, com pontuação de leads,
geração de emails de outreach personalizados com IA (com revisão humana antes
do envio) e um dashboard de métricas.

Projeto de portefólio — construído como se fosse um projeto real para cliente,
seguindo um processo profissional completo: arquitetura → stack →
implementação → testes → Docker → deployment → documentação → apresentação
comercial.

## Estado do projeto

| Fase | Estado |
|---|---|
| 1. Arquitetura | ✅ Concluída |
| 2. Stack tecnológico | ✅ Concluída |
| 3. Repositório | 🔄 Em curso |
| 4. Implementação | ⬜ Por iniciar |
| 5. Testes & Docker | ⬜ Por iniciar |
| 6. Deployment | ⬜ Por iniciar |
| 7. Documentação | ⬜ Por iniciar |
| 8. Apresentação comercial | ⬜ Por iniciar |

## Arquitetura (resumo)

```
Agendador → Google Places API → Processamento & scoring → PostgreSQL
                                                               │
                              ┌────────────────────────────────┼──────────┐
                              ▼                                          ▼
                    Geração de email (IA)                      Dashboard (React)
                              │
                              ▼
                    Revisão humana & envio (Resend, com opt-out RGPD)
```

Ver [`docs/architecture.md`](docs/architecture.md) para o detalhe.

## Stack tecnológico

**Backend:** Python 3.12 · FastAPI · SQLAlchemy 2.0 (async) · Alembic ·
Pydantic v2 · APScheduler · PostgreSQL 16

**Frontend:** React 18 · TypeScript · Vite · TanStack Query · Recharts ·
Tailwind CSS

**Integrações externas:** Google Places API (New) · Claude API (Anthropic) ·
Resend (email transacional)

**Qualidade & DevOps:** pytest · Ruff · mypy · Docker & Docker Compose ·
GitHub Actions

## Estrutura do repositório

```
.
├── backend/           # API FastAPI, modelos, serviços, scheduler
│   ├── app/
│   │   ├── api/routes/        # Endpoints REST
│   │   ├── core/              # Configuração, ligação à base de dados
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Modelos Pydantic (request/response)
│   │   ├── services/
│   │   │   ├── ingestion/     # Cliente Google Places (adaptador)
│   │   │   ├── scoring/       # Limpeza, deduplicação, pontuação de leads
│   │   │   ├── ai_generation/ # Geração de emails com Claude
│   │   │   └── email/         # Envio via Resend
│   │   └── scheduler/         # Jobs periódicos (APScheduler)
│   ├── alembic/                # Migrações da base de dados
│   └── tests/
├── frontend/           # Dashboard React
│   └── src/
│       ├── api/                # Clientes HTTP + hooks TanStack Query
│       ├── components/
│       ├── hooks/
│       └── pages/
├── docs/               # Documentação técnica e decisões de arquitetura
└── .github/workflows/  # CI (lint + testes)
```

## Como correr o projeto

> Instruções completas chegam na fase 4 (implementação) e fase 6 (deployment).
> Por agora, este repositório contém o esqueleto profissional do projeto.

```bash
# Backend
cd backend
uv sync
cp .env.example .env   # preencher as chaves de API

# Frontend
cd frontend
npm install
```

## Licença

Projeto de portefólio pessoal de Luís — todos os direitos reservados.
