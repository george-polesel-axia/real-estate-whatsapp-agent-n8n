# Relatorio de Migrations Supabase

Data: 2026-06-29

## Projeto

- Host SQL: `db.wyebbjtkmpgijktosryj.supabase.co`
- Banco: `postgres`
- PostgreSQL: `17.6`
- Observacao de rede: o host direto resolveu apenas IPv6 no ambiente local. A aplicacao foi feita usando o servidor n8n como cliente SQL, pois ele possui conectividade IPv6.

## Migrations Aplicadas

Aplicadas em ordem:

1. `001_extensions.sql`
2. `002_schema.sql`
3. `003_indexes.sql`
4. `004_rls_policies.sql`
5. `005_rpc_functions.sql`
6. `006_seed_sample_data.sql`

## Extensoes

- `uuid-ossp` ja existia.
- `pg_trgm` habilitada.
- `vector` habilitada.

Versoes verificadas:

- `pg_trgm`: `1.6`
- `uuid-ossp`: `1.1`
- `vector`: `0.8.0`

## Tabelas Criadas

- `real_estate_agencies`
- `brokers`
- `clients`
- `properties`
- `property_media`
- `property_features`
- `property_embeddings`
- `client_conversations`
- `conversation_messages`
- `appointments`
- `agent_handoffs`
- `agent_events`
- `agent_failures`
- `agent_settings`

## Indices e RLS

- Indices estruturados criados para busca por bairro, rua, tipo, dormitorios, vagas, status, preco e telefone.
- Indices GIN/trigram criados para busca textual.
- Indice HNSW criado em `property_embeddings.embedding`.
- RLS habilitado nas 14 tabelas do projeto.

## RPCs Criadas

- `match_properties`
- `search_properties_hybrid`

## Seed de Teste

Registros inseridos:

- Agencias: 1
- Corretores: 1
- Imoveis: 4
- Midias: 2

## Validacao Executada

Consulta de teste:

```sql
select property_id, title, street, total_score
from search_properties_hybrid(
  '00000000-0000-0000-0000-000000000001',
  'sobrado alto do ipiranga 3 dormitorios portao azul',
  'Alto do Ipiranga',
  null,
  'sobrado',
  3,
  2,
  'venda',
  null,
  null,
  3,
  null
);
```

Resultado validado:

1. `Sobrado na Rua Bento Vieira com portao azul`
2. `Sobrado na Arcipreste Andrade`

O primeiro resultado corresponde ao comportamento esperado para a pista "portao azul".

## Seguranca

- Nenhuma credencial foi gravada no repositorio.
- Nenhum comando destrutivo foi executado.
- Nao houve `DROP`, `TRUNCATE`, `DELETE` em massa ou desativacao de RLS.
- A senha compartilhada no chat deve ser trocada.
