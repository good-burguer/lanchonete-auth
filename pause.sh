#!/usr/bin/env bash
set -euo pipefail

source .env

echo "[pause] Destruindo infraestrutura do módulo de autenticação via AWS SAM..."

sam delete --stack-name "$SAM_STACK_NAME" --region "$AWS_REGION" --no-prompts

echo "[pause] Forçando remoção do segredo jwtSecret..."
aws secretsmanager delete-secret \
  --secret-id "jwtSecret" \
  --region "$AWS_REGION" \
  --force-delete-without-recovery || echo "[pause] ⚠️ Segredo jwtSecret não encontrado ou já excluído."

echo "[pause] ✅ Stack do SAM removida com sucesso."