#!/usr/bin/env bash
set -euo pipefail

REPOS=("lanchonete-infra" "lanchonete-database" "lanchonete-app" "lanchonete-auth")

for R in "${REPOS[@]}"; do
  echo ">>> Configurando $R"
  cd "$R"

  case "$R" in
    lanchonete-infra)
      mkdir -p modules/{vpc,eks,ecr} environments/dev .github/workflows
      printf "" > modules/vpc/.gitkeep
      printf "" > modules/eks/.gitkeep
      printf "" > modules/ecr/.gitkeep

      cat > environments/dev/backend.tf <<'HCL'
terraform {
  backend "s3" {
    bucket         = var.tf_state_bucket
    key            = "infra/terraform.tfstate"
    region         = var.aws_region
    dynamodb_table = var.tf_lock_table
    encrypt        = true
  }
}
HCL

      cat > environments/dev/main.tf <<'HCL'
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
provider "aws" { region = var.aws_region }
HCL

      cat > environments/dev/variables.tf <<'HCL'
variable "aws_region"      { type = string }
variable "tf_state_bucket" { type = string }
variable "tf_lock_table"   { type = string }
HCL

      cat > environments/dev/outputs.tf <<'HCL'
output "region" { value = var.aws_region }
HCL

      cat > README.md <<'MD'
# Lanchonete – Infra (Terraform)
Infra do EKS/VPC/ECR via Terraform.

## Estrutura
- `modules/` módulos reutilizáveis
- `environments/dev` entrada do ambiente
- `.github/workflows/` pipelines

## Como validar
1. Defina VARS no repo: `AWS_REGION`, `TF_STATE_BUCKET`, `TF_LOCK_TABLE`
2. O CI rodará `terraform init/validate/plan` em PR e `apply` no merge.
MD
      ;;

    lanchonete-database)
      mkdir -p modules/rds-postgres environments/dev .github/workflows
      printf "" > modules/rds-postgres/.gitkeep

      cat > environments/dev/backend.tf <<'HCL'
terraform {
  backend "s3" {
    bucket         = var.tf_state_bucket
    key            = "database/terraform.tfstate"
    region         = var.aws_region
    dynamodb_table = var.tf_lock_table
    encrypt        = true
  }
}
HCL

      cat > environments/dev/main.tf <<'HCL'
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
provider "aws" { region = var.aws_region }
HCL

      cat > environments/dev/variables.tf <<'HCL'
variable "aws_region"      { type = string }
variable "tf_state_bucket" { type = string }
variable "tf_lock_table"   { type = string }
HCL

      cat > environments/dev/outputs.tf <<'HCL'
output "region" { value = var.aws_region }
HCL

      cat > README.md <<'MD'
# Lanchonete – Database (Terraform)
Infra de RDS Postgres via Terraform (state S3 + lock DynamoDB).

## Estrutura
- `modules/rds-postgres` módulo do banco
- `environments/dev` ambiente
MD
      ;;

    lanchonete-app)
      mkdir -p app charts/app migrations .github/workflows
      printf "" > migrations/.gitkeep

      cat > app/__init__.py <<'PY'
print("lanchonete-app package")
PY

      cat > charts/app/Chart.yaml <<'YAML'
apiVersion: v2
name: lanchonete-app
version: 0.1.0
appVersion: "0.1.0"
YAML

      cat > Dockerfile <<'DOCKER'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt || true
COPY app/ /app/app
CMD ["python","-c","print('lanchonete-app up')"]
DOCKER

      cat > requirements.txt <<'REQ'
# adicione suas libs aqui (ex.: fastapi, uvicorn, psycopg2-binary, pydantic, ...)
REQ

      cat > README.md <<'MD'
# Lanchonete – App
Aplicação (ex.: FastAPI) implantada no EKS via Helm.

## Estrutura
- `app/` código da aplicação
- `charts/app/` chart Helm
- `migrations/` migrações (Alembic)

## CI (depois)
- VARS: `AWS_REGION`, `AWS_ACCOUNT_ID`, `EKS_CLUSTER`
- SECRET: `AWS_ROLE_APP`
MD
      ;;

    lanchonete-auth)
      mkdir -p src .github/workflows

      cat > src/handler.py <<'PY'
def handler(event, context):
    params = (event.get("queryStringParameters") or {})
    cpf = params.get("cpf")
    return {"statusCode": 200, "body": f"OK - cpf={cpf}"}
PY

      cat > template.yaml <<'YAML'
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Lanchonete Auth (CPF)
Resources:
  AuthFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handler.handler
      Runtime: python3.12
      MemorySize: 256
      Timeout: 10
      Events:
        Api:
          Type: Api
          Properties:
            Path: /auth
            Method: get
YAML

      cat > requirements.txt <<'REQ'
# dependências da Lambda (ex.: boto3) - adicione conforme necessário
REQ

      cat > README.md <<'MD'
# Lanchonete – Auth (Lambda)
Lambda exposta no API Gateway para autenticação por CPF (SAM).
MD
      ;;
  esac

  git add .
  git commit -m "chore: estrutura mínima (Item 2)"
  # tenta push; se a branch estiver protegida, você pode abrir um PR depois
  git push origin main || true

  cd ..
done

echo "Tudo pronto. Verifique cada repo no GitHub para confirmar os arquivos."
