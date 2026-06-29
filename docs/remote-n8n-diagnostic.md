# Diagnostico do n8n Remoto

Data: 2026-06-29

## Host

- Servidor: `168.231.89.175`
- Hostname: `srv1005345`
- Sistema: Ubuntu 24.04.3 LTS

## n8n

- Container Docker encontrado: `n8n-n8n-1`
- Imagem: `docker.n8n.io/n8nio/n8n:stable`
- Versao reportada pelo CLI: `2.6.4`
- Processo adicional no host tambem encontrado executando `/usr/local/bin/n8n`; revisar depois se ele ainda e necessario.
- Workflows existentes antes da importacao: 76
- Backup criado no servidor: `/root/backups/n8n/backup-20260629-092612`
- Workflows apos importacao: 80

## Workflows importados

Todos foram importados com `active=false`:

- `Real Estate Agent Main`
- `Real Estate Agent Calendar`
- `Real Estate Agent Ingestion`
- `Real Estate Agent Human Handoff`

## WhatsApp

- Container WAHA encontrado: `n8n-waha-1`
- Imagem: `devlikeapro/waha:latest`
- Porta local publicada no host: `3100:3000`

## Dominios

- `https://n8n.axiaia.com.br/` respondeu HTTP 200 no servidor.
- `https://n8neditor.ialuno.com.br/` respondeu HTTP 200 no servidor.
- O `docker-compose.yml` do servidor ainda contem configuracao Traefik explicita para `n8neditor.ialuno.com.br`. Revisar se `n8n.axiaia.com.br` esta configurado fora desse compose, em DNS/proxy externo ou em outra regra.

## Observacoes de seguranca

- O compose remoto contem secrets em texto claro para outros servicos. Nao foram copiados para este repositorio.
- A senha SSH usada nesta sessao deve ser trocada.
- Antes de ativar workflow em producao, configurar credenciais n8n e executar teste end-to-end.
