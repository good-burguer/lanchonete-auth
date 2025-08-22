def handler(event, context):
    params = (event.get("queryStringParameters") or {})
    cpf = params.get("cpf")
    return {"statusCode": 200, "body": f"OK - cpf={cpf}"}
