# Setup WhatsApp

O workflow principal usa webhook generico e normalizacao defensiva. O provedor ativo e definido por `WHATSAPP_PROVIDER`.

## WhatsApp Cloud API

Use:

- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_VERIFY_TOKEN`

Envio de mensagem: `POST https://graph.facebook.com/v20.0/{phone_number_id}/messages`.

## WAHA

Use:

- `WAHA_BASE_URL`
- `WAHA_API_KEY`

Adapte o node de envio para o endpoint da sessao configurada.

## Evolution API

Use:

- `EVOLUTION_BASE_URL`
- `EVOLUTION_API_KEY`

Adapte o node de envio para a instancia Evolution e formato esperado.

## Midias

O contrato interno espera `media.url`, `media.id`, `media.mime_type` e `message_type`. Quando o provedor so entregar ID, adicione node HTTP para resolver a URL temporaria antes da transcricao/analise.
