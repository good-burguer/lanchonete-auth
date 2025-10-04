import json
import os
import boto3
import jwt
from datetime import datetime, timedelta, timezone
from validar_cpf import validar_cpf

def get_jwt_secret():
    secret_name = os.getenv("JWT_SECRET_NAME")
    region = os.getenv("AWS_REGION", "us-east-1")

    client = boto3.client('secretsmanager', region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response.get('SecretString')
    return secret_string if secret_string else response['SecretBinary']

def handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        cpf_cliente = body.get("cpf")

        if not cpf_cliente:
            return {
                "statusCode": 400,
                "body": json.dumps({"success": False, "error": "CPF é obrigatório"})
            }

        if not validar_cpf(cpf_cliente):
            return {
                "statusCode": 400,
                "body": json.dumps({"success": False, "error": "CPF inválido"})
            }

        # Consulta no Cognito User Pool
        cognito = boto3.client('cognito-idp')
        user_pool_id = os.getenv("USER_POOL_ID")
        usuarios = cognito.list_users(
            UserPoolId=user_pool_id,
            Filter=f'username = "{cpf_cliente}"'
        )

        if not usuarios['Users']:
            return {
                "statusCode": 404,
                "body": json.dumps({"success": False, "error": "CPF não encontrado"})
            }

        nome = ""
        for attr in usuarios['Users'][0]['Attributes']:
            if attr['Name'] == 'name':
                nome = attr['Value']

        # Gera JWT com segredo do Secrets Manager
        secret = get_jwt_secret()
        payload = {
            "sub": cpf_cliente,
            "nome": nome,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        token = jwt.encode(payload, secret, algorithm="HS256")

        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "token": token})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "error": str(e)})
        }
