#!/usr/bin/env bash
set -euo pipefail

: "${N8N_BASE_URL:?N8N_BASE_URL is required}"
: "${N8N_API_KEY:?N8N_API_KEY is required}"

mkdir -p backups/n8n
curl -fsS \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  "${N8N_BASE_URL%/}/api/v1/workflows" \
  > "backups/n8n/workflows-$(date +%Y%m%d-%H%M%S).json"
