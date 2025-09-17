import json
from src.rule.validar_cpf import validar_cpf
from src.db.conexao import conexao, conn

def autenticacao(event, context):
    
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

        consulta_cliente = conexao.execute("SELECT nome, cpf FROM cliente WHERE cpf = %s", (cpf_cliente,))
        retorno_consulta_cliente = conexao.fetchone()
        
        conexao.close()
        conn.close()

        if not retorno_consulta_cliente:
            return {
                "statusCode": 404,
                "body": json.dumps({"success": False, "error": "CPF não encontrado"})
            }
            
        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "cliente": consulta_cliente.nome})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "error": str(e)})
        }
