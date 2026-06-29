# Troubleshooting

## Workflow nao importa

Rode `node scripts/validate-n8n-workflows.js` e confira se o JSON tem `nodes` e `connections`.

## Supabase bloqueia acesso

Confira se a tabela esta exposta na Data API, se os grants existem e se a RLS tem policy adequada.

## Busca vetorial nao retorna

Confirme que `property_embeddings.embedding` tem 1536 dimensoes e que a extensao `vector` esta habilitada.

## WhatsApp nao responde

Valide token, phone number ID, URL base do provedor e formato do payload.

## Calendario nao agenda

Confirme refresh token, escopos OAuth, calendario do corretor e timezone.
