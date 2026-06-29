# Real Estate WhatsApp Agent n8n

Agente imobiliario via WhatsApp orquestrado no n8n, com persistencia no Supabase Postgres/pgvector, integracao com Google Calendar, confirmacao por WhatsApp/e-mail e versionamento no GitHub.

O projeto esta estruturado para começar com webhook generico de WhatsApp. A adaptacao para WhatsApp Cloud API, WAHA ou Evolution API fica concentrada nos nodes de normalizacao e envio de mensagem.

## Arquitetura

Fluxo principal:

1. WhatsApp chama o webhook do n8n.
2. O workflow normaliza o payload e identifica texto, audio, video ou imagem.
3. Midias sao baixadas quando o provedor disponibiliza URL ou ID.
4. Audio/video podem ser transcritos por modelo configuravel.
5. Cliente, conversa e mensagens sao persistidos no Supabase.
6. O agente extrai intencao e atributos do imovel.
7. A consulta recebe embedding e chama `search_properties_hybrid`.
8. O agente desambigua, apresenta detalhes, oferece visita ou aciona handoff.
9. O subfluxo de calendario consulta/cria evento no Google Calendar.
10. Confirmacoes sao enviadas por WhatsApp e e-mail.
11. Eventos, falhas e auditoria ficam registrados no Supabase.

## Pre-requisitos

- n8n remoto com Webhook, HTTP Request, Code e credenciais para OpenAI, Supabase, Google e e-mail.
- Supabase com Postgres e extensoes `vector` e `pg_trgm` habilitaveis.
- Provedor WhatsApp: Cloud API, WAHA, Evolution API ou equivalente.
- Credenciais OAuth do Google Calendar.
- SMTP, Gmail ou e-mail corporativo.
- Node.js para validar workflows e rodar simulacoes locais.

## Variaveis de ambiente

Copie `.env.example` para `.env` fora do Git e preencha localmente. Nunca commite `.env` ou secrets reais.

As variaveis cobrem n8n, WhatsApp, Supabase, Google Calendar, SMTP e OpenAI. O workflow usa placeholders e nomes de credenciais para serem configurados no n8n.

## Configurar Supabase

1. Abra o SQL Editor do Supabase.
2. Rode as migrations em ordem:
   - `supabase/migrations/001_extensions.sql`
   - `supabase/migrations/002_schema.sql`
   - `supabase/migrations/003_indexes.sql`
   - `supabase/migrations/004_rls_policies.sql`
   - `supabase/migrations/005_rpc_functions.sql`
   - `supabase/migrations/006_seed_sample_data.sql`
3. Valide as tabelas e RPCs conforme `docs/setup-supabase.md`.

Impacto: as migrations criam extensoes, tabelas, FKs, indices, RLS, funcoes RPC e dados ficticios. Nao apagam tabelas nem dados existentes.

## Rodar migrations

Em projeto limpo, rode os SQLs na ordem acima. Se usar CLI Supabase, aplique cada arquivo com `psql` usando `SUPABASE_DB_URL` em ambiente local seguro:

```bash
psql "$SUPABASE_DB_URL" -f supabase/migrations/001_extensions.sql
psql "$SUPABASE_DB_URL" -f supabase/migrations/002_schema.sql
psql "$SUPABASE_DB_URL" -f supabase/migrations/003_indexes.sql
psql "$SUPABASE_DB_URL" -f supabase/migrations/004_rls_policies.sql
psql "$SUPABASE_DB_URL" -f supabase/migrations/005_rpc_functions.sql
psql "$SUPABASE_DB_URL" -f supabase/migrations/006_seed_sample_data.sql
```

## Configurar n8n

1. Importe os arquivos em `n8n/workflows/`.
2. Crie credenciais conforme `n8n/credentials-template/credentials-map.md`.
3. Configure variaveis do n8n ou credenciais internas.
4. Teste manualmente com os payloads em `n8n/test-payloads/`.
5. Ative apenas depois de validar em ambiente de teste.

## Importar workflows

Pelo n8n UI: `Workflows > Import from File`.

Via API, depois de fornecer `N8N_BASE_URL` e `N8N_API_KEY`, use:

```bash
scripts/import-n8n-workflows.sh
```

Antes de alterar workflow existente em producao, exporte backup:

```bash
scripts/export-n8n-workflows.sh
```

## Configurar WhatsApp

O workflow principal assume webhook generico e resposta por node HTTP configuravel.

- Cloud API: use `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID` e `WHATSAPP_VERIFY_TOKEN`.
- WAHA: use `WAHA_BASE_URL` e `WAHA_API_KEY`.
- Evolution API: use `EVOLUTION_BASE_URL` e `EVOLUTION_API_KEY`.

Detalhes em `docs/setup-whatsapp.md`.

## Configurar Google Calendar

Crie OAuth Client, obtenha refresh token, defina `GOOGLE_CALENDAR_ID` ou calendario por corretor em `brokers.google_calendar_id`. Veja `docs/setup-google-calendar.md`.

## Configurar e-mail

Use SMTP ou Gmail. Defina `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` e `SMTP_FROM`. O workflow de calendario envia confirmacao ao cliente e notifica corretor.

## Cadastrar imoveis

Use o workflow `real-estate-agent-ingestion.json` via webhook/manual, ou rode inserts SQL. O seed ficticio cria imoveis para os cenarios de teste.

## Gerar embeddings

Configure `OPENAI_API_KEY` e `SUPABASE_DB_URL` localmente, depois rode:

```bash
node scripts/generate-property-embeddings.js
```

O script esta preparado para ambiente real, mas nao inclui credenciais.

## Testar conversa simulada

```bash
node scripts/validate-n8n-workflows.js
node scripts/run-simulation-tests.js
```

O relatorio e gravado em `tests/test-report.md`.

## Ativar em producao

1. Confirme backup dos workflows atuais.
2. Rode teste end-to-end com numero WhatsApp de homologacao.
3. Valide logs em `agent_events` e `agent_failures`.
4. Ative o workflow principal no n8n somente apos aprovacao.

## Backup

- Exporte workflows n8n antes de qualquer alteracao.
- Mantenha migrations versionadas.
- Use backups nativos do Supabase para banco de producao.

## Problemas comuns

- Tabela inacessivel pela API: confira Data API, grants e RLS.
- RPC sem resultado: confirme embeddings 1536 dimensoes e filtros.
- WhatsApp nao envia: confira provedor e token.
- Calendar nao cria evento: confira refresh token e calendario do corretor.
- Workflow nao importa: rode `node scripts/validate-n8n-workflows.js`.
