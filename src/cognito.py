# src/cognito.py
import os
import boto3

# Inicializa o cliente da AWS para interagir com o Cognito
cognito_client = boto3.client('cognito-idp', region_name=os.getenv("AWS_REGION"))
USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID") # Pega o ID do User Pool que o Terraform vai nos dar

def consultar_usuario_cognito(cpf: str):
    """
    Consulta se um usuário com um determinado CPF existe no Cognito.
    Isto cumpre o requisito de integração do projeto.
    """
    try:
        # Esta busca depende de um atributo customizado chamado 'cpf' no seu User Pool
        response = cognito_client.list_users(
            UserPoolId=USER_POOL_ID,
            Filter=f"custom:cpf = \"{cpf}\""  # Procura por um usuário com o CPF correspondente
        )
        # Se a lista de usuários retornada não for vazia, significa que o usuário existe
        usuario_existe = len(response.get('Users', [])) > 0
        print(f"Consulta no Cognito para o CPF {cpf}: {'Encontrado' if usuario_existe else 'Não encontrado'}")
        return usuario_existe

    except Exception as e:
        print(f"AVISO: Erro ao consultar usuário no Cognito: {e}")
        # Conforme nossa regra, uma falha na consulta ao Cognito não impede o login,
        # pois a fonte principal da verdade é o nosso banco de dados.
        # Apenas registramos o erro para que a equipe possa monitorar.
        return False