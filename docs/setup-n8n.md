# Setup n8n

## Importacao

Importe estes arquivos pelo n8n UI:

- `n8n/workflows/real-estate-agent-main.json`
- `n8n/workflows/real-estate-agent-ingestion.json`
- `n8n/workflows/real-estate-agent-calendar.json`
- `n8n/workflows/real-estate-agent-human-handoff.json`

## Credenciais

Crie credenciais para:

- OpenAI ou modelo compativel.
- Supabase REST/PostgREST.
- WhatsApp provider escolhido.
- Google Calendar OAuth.
- SMTP/Gmail.

Use `n8n/credentials-template/credentials-map.md` como checklist.

## Validacao

Rode:

```bash
node scripts/validate-n8n-workflows.js
```

Teste o webhook com os payloads em `n8n/test-payloads/`.

## Producao

Nao ative workflows em producao sem teste end-to-end. Antes de modificar workflow existente, exporte backup e versiona o JSON.
