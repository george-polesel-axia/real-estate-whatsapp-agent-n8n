# Reflexo do Estado Remoto n8n

Data: 2026-06-29

## Acao

Os workflows remotos do n8n foram exportados e os JSONs em `n8n/workflows/` foram atualizados para refletir o estado atual da instancia.

## Workflows refletidos

- `Real Estate Agent Main`
- `Real Estate Agent Ingestion`
- `Real Estate Agent Calendar`
- `Real Estate Agent Human Handoff`
- `Real Estate Agent Main Mock`

## Estado remoto observado

Todos os workflows exportados estavam `active=false`.

Credenciais observadas no export:

- `Real Estate Agent Main`: `Supabase Real Estate REST`
- `Real Estate Agent Ingestion`: `Supabase Real Estate REST`
- `Real Estate Agent Calendar`: nenhuma credencial no export
- `Real Estate Agent Human Handoff`: nenhuma credencial no export
- `Real Estate Agent Main Mock`: nenhuma credencial no export

## Observacao

O nome informado para Supabase foi `db_dev`, mas o export remoto do n8n ainda mostra `Supabase Real Estate REST` nos nodes HTTP de Supabase. Isso pode significar que:

- a credencial real foi ajustada dentro de uma credencial com nome antigo; ou
- os nodes ainda precisam ser apontados manualmente para `db_dev` no n8n.

Antes de ativar em producao, revisar essa associacao no editor do n8n.

## Seguranca

O export de workflow nao incluiu valores secretos de credenciais. Mesmo assim, os workflows permanecem inativos ate teste end-to-end controlado.
