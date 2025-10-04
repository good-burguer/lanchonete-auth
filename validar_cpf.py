def validar_cpf(cpf: str) -> bool:
    
    """verificar se o cpf é válido"""
    
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    
    digito1 = (soma * 10 % 11) % 10
    
    if digito1 != int(cpf[9]):
        return False
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    
    digito2 = (soma * 10 % 11) % 10
    
    if digito2 != int(cpf[10]):
        return False
    
    return True
