#!/usr/bin/env bash

set -euo pipefail

# Verifica se o arquivo .env existe
if [ ! -f .env ]; then
  echo "[resume] ❌ Arquivo .env não encontrado. Abortando."
  exit 1
fi


# Carrega variáveis de ambiente do arquivo .env (não versionado)
source .env

# Verifica se a variável JWT_SECRET_VALUE está definida
if [ -z "${JWT_SECRET_VALUE:-}" ]; then
  echo "[resume] ❌ Variável JWT_SECRET_VALUE não está definida no .env."
  exit 1
fi

echo "[resume] Subindo infraestrutura do módulo de autenticação via AWS SAM..."

sam build
sam deploy --stack-name "$SAM_STACK_NAME" --region "$AWS_REGION" --config-file samconfig.toml --no-confirm-changeset --no-fail-on-empty-changeset --parameter-overrides JwtSecretValue="$JWT_SECRET_VALUE"

echo "[resume] ✅ Stack do SAM implantada com sucesso."