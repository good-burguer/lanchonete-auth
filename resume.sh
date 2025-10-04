#!/usr/bin/env bash
set -euo pipefail

# Carrega variáveis de ambiente do arquivo .env (não versionado)
source .env

echo "[resume] Subindo infraestrutura do módulo de autenticação via AWS SAM..."

sam build
sam deploy --stack-name "$SAM_STACK_NAME" --region "$AWS_REGION" --config-file samconfig.toml --no-confirm-changeset --no-fail-on-empty-changeset

echo "[resume] ✅ Stack do SAM implantada com sucesso."