# Bindings de Credenciais n8n

Data: 2026-06-29

## Credenciais atuais

- Supabase: `db_dev`
- WAHA: `waha`
- OpenAI: `openai_gp`
- Google Calendar: `google_cal_dev`
- E-mail provisorio: `george.polesel@gmail.com`
- Credencial de teste permitida: `teste_codex`

## Estado conhecido

- `waha` esta com falha e depende de troca/configuracao de numero de telefone.
- O e-mail e provisorio e deve ser substituido antes de producao.
- Se uma credencial operacional falhar durante testes, pode ser criada/acionada `teste_codex` para teste, sem apagamento automatico.

## Impacto nos workflows

Os workflows versionados foram ajustados para referenciar `db_dev` nos nodes HTTP de Supabase.

Os nodes de WhatsApp, OpenAI, Google Calendar e e-mail ainda devem ser conectados no n8n conforme a credencial real estiver valida. Enquanto `waha` estiver instavel, os workflows devem permanecer inativos ou rodar apenas com payloads simulados.

## Teste sem credenciais reais

Para testar enquanto `waha`/OpenAI/Calendar/e-mail nao estiverem prontos, use o workflow:

- `Real Estate Agent Main Mock`

Esse workflow responde pelo webhook `/webhook/real-estate-agent/mock`, usa dados ficticios locais e nao chama Supabase, WhatsApp, OpenAI, Google Calendar ou SMTP. Ele serve apenas para validar fluxo conversacional e importabilidade no n8n.
