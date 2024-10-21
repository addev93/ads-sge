import logging
logging.basicConfig(level=logging.INFO)

class MovementValidator:

    def check_movement_operation(balance_manager, product_id, quantity, type_id):
        """Verifica se a movimentação resulta em saldo negativo."""
        current_balance = balance_manager.search_product_balance(product_id) # Saldo atual do produto
        if type_id == 2: # Operação do tipo "StockOut"
            if current_balance:
                if (current_balance - quantity) < 0:
                    logging.warning(f'ServiceMovementManager: Operação não permitida pois resulta em saldo negativo. Menor valor permitido: {current_balance}.')
                    return False
                else:
                    return True
            else:
                logging.warning(f'ServiceMovementManager: Operação não permitida pois resulta em saldo negativo. Primeiro registre um movimento de entrada do produto.')
                return True
        else:
            return True
            
    def check_delete_operation(manager, movement_code):
        """Verifica se o operação de delete resulta em saldo negativo."""
        movement = manager.movements_repos_manager.search_by_code(movement_code)
        if not movement:
            logging.info(f'CheckMovementOperation: Nenhum movimento encontrado para o código {movement_code}.')
            return False
        else:
            product_id = movement[2]
            quantity = movement[3]
            current_balance = manager.balance_manager.search_product_balance(product_id)
            if (current_balance - quantity) < 0:
                logging.warning(f'CheckMovementsOperations: Operação não permitida pois o saldo resultante é negativo.')
                return False
            else:
                return True