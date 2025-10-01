# src/jwt_handler.py
import os
import jwt
import datetime

def gerar_token(cpf: str, nome: str) -> str:
    """
    Gera um token JWT para o cliente autenticado.
    Este token será usado para proteger as outras rotas da API.
    """
    
    # O "payload" são as informações que queremos guardar dentro do token
    payload = {
        'sub': cpf,                                                   # 'subject' (sujeito), o identificador único do usuário. Usamos o CPF.
        'name': nome,                                                 # Nome do usuário, para conveniência.
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1), # 'expiration time', quando o token expira (configurado para 1 hora).
        'iat': datetime.datetime.utcnow()                             # 'issued at', quando o token foi criado.
    }
    
    # O segredo é uma "chave" que usamos para assinar o token, garantindo que ele não foi modificado.
    # Ele será passado pelo Terraform através das variáveis de ambiente.
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise ValueError("ERRO CRÍTICO: JWT_SECRET não foi configurado nas variáveis de ambiente.")

    # Codifica o payload usando o segredo e o algoritmo HS256
    token = jwt.encode(payload, secret, algorithm="HS256")
    
    return token