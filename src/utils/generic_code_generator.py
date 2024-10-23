import datetime

def generate_code(registers, prefix):
    """
    Gera automaticamente o código de um determinado registro.

    Args:
        registers (list): Uma lista de códigos já existentes registrados na tabela.
        prefix (str): Um prefixo a ser adicionado ao código gerado.

    Returns:
        str: O código gerado para o novo registro.

    Example:
        >>> existing_registers = [(REG2402001,), (REG2402002,)]
        >>> code = generate_code(existing_registers, 'REG')
        >>> print(code)
        'REG2402003'
    """

    # Obtém o ano e mês atuais
    now = datetime.datetime.now()
    year = now.strftime('%y')   # Últimos dois dígitos do ano
    month = now.strftime('%m')  # Mês no formato "00"

    # Conta o número de registros do período atual
    current_month_requests = []
    for code in registers:
        period = code.replace(prefix, '')[:4] # Remove o prefixo e obtem o ano-mês
        if period == f'{year}{month}':
            current_month_requests.append(code) # Considera os 7 primeiros caracteres do código

    # Gera o número sequencial
    sequence_number = len(current_month_requests) + 1
    sequence = f'{sequence_number:06}'  # Formata como 6 dígitos

    # Monta o código final
    purchase_request_code = f'{prefix}{year}{month}{sequence}'
    
    return purchase_request_code