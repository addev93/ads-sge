import datetime

def generate_movement_code(movements):
    """Gera automaticamente o código do movimento no formato MOVYYMMXXXXXX."""
    # Obtém o ano e mês atuais
    now = datetime.datetime.now()
    year = now.strftime('%y')  # Últimos dois dígitos do ano
    month = now.strftime('%m')  # Mês no formato "00"

    # Conta o número de movimentações do período atual
    current_month_movements = []
    for mov in movements:
        if mov[1][:7] == f'MOV{year}{month}':
            current_month_movements.append(mov)  # Considera os 7 primeiros caracteres do código

    # Gera o número sequencial
    sequence_number = len(current_month_movements) + 1
    sequence = f'{sequence_number:06}'  # Formata como 6 dígitos

    # Monta o código final
    movement_code = f'MOV{year}{month}{sequence}'
    
    return movement_code