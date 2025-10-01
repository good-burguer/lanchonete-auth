# src/db.py (versão final e segura)
import os
import boto3
import json
import pg8000.dbapi

def get_db_connection():
    """
    Busca as credenciais do banco no AWS Secrets Manager e retorna uma nova conexão.
    """
    secret_name = os.getenv("DB_SECRET_NAME")
    region_name = os.getenv("AWS_REGION")

    # Cria um cliente do Secrets Manager
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        # Busca o valor do segredo
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret_string = get_secret_value_response['SecretString']
        secret = json.loads(secret_string)
        
        # Usa as credenciais do segredo para conectar
        conn = pg8000.dbapi.connect(
            host=secret['host'],
            database=secret['dbname'],
            user=secret['username'],
            password=secret['password'],
            port=secret['port']
        )
        return conn
    except Exception as e:
        print(f"Erro ao obter segredo ou conectar ao banco de dados: {e}")
        raise e