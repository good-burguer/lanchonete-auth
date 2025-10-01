# handler.py (versão final)
import json
import os
from src.validator import validar_cpf
from src.db import get_db_connection
from src.cognito import consultar_usuario_cognito
from src.jwt_handler import gerar_token

def lambda_handler(event, context):
    conn = None
    try:
        body = json.loads(event.get("body") or "{}")
        cpf_cliente = body.get("cpf")

        if not cpf_cliente or not validar_cpf(cpf_cliente):
            return {"statusCode": 400, "body": json.dumps({"error": "CPF inválido ou não fornecido"})}

        conn = get_db_connection()
        cliente_db = None
        with conn.cursor() as cursor:
            cursor.execute("SELECT nome, cpf FROM cliente WHERE cpf = %s", (cpf_cliente,))
            result = cursor.fetchone()
            if result:
                cliente_db = {"nome": result[0], "cpf": result[1]}

        if not cliente_db:
            return {"statusCode": 404, "body": json.dumps({"error": "Cliente não encontrado"})}

        consultar_usuario_cognito(cpf_cliente)

        token = gerar_token(cpf=cliente_db["cpf"], nome=cliente_db["nome"])

        return {
            "statusCode": 200,
            "body": json.dumps({"token": token})
        }

    except Exception as e:
        print(f"ERRO: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": "Erro interno do servidor"})}
    finally:
        if conn:
            conn.close()