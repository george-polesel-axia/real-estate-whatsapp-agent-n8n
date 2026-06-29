# Setup Supabase

## Ordem de execucao

1. `001_extensions.sql`
2. `002_schema.sql`
3. `003_indexes.sql`
4. `004_rls_policies.sql`
5. `005_rpc_functions.sql`
6. `006_seed_sample_data.sql`

## Extensoes

`vector` e `pg_trgm` sao criadas com `create extension if not exists`. Em Supabase, `vector` pode ficar no schema `extensions`, mas o tipo `vector(1536)` fica disponivel para uso no SQL.

## RLS

Todas as tabelas publicas recebem RLS. As policies permitem acesso do `service_role` para automacoes servidor-servidor e leitura basica autenticada por agencia quando houver claim `agency_id` em `app_metadata`.

## Validar RPCs

Depois do seed, rode:

```sql
select *
from search_properties_hybrid(
  (select id from real_estate_agencies limit 1),
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

Sem embedding, a funcao usa scores textual e estruturado. Com embedding, soma similaridade vetorial.
