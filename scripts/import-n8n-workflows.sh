#!/usr/bin/env bash
set -euo pipefail

: "${N8N_BASE_URL:?N8N_BASE_URL is required}"
: "${N8N_API_KEY:?N8N_API_KEY is required}"

for file in n8n/workflows/*.json; do
  curl -fsS \
    -X POST \
    -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
    -H "Content-Type: application/json" \
    --data-binary "@${file}" \
    "${N8N_BASE_URL%/}/api/v1/workflows"
  printf '\nImported %s\n' "$file"
done
