import logging
logging.basicConfig(level=logging.INFO)
from src.repositories.repos_movements import RepositoryMovementManager
from src.repositories.repos_movement_types import RepositoryMovementTypes
from src.repositories.repos_products import RepositoryProductManager
from src.repositories.repos_inventory_balances import RepositoryInventoryBalances
from src.utils.movement_code_generator import generate_movement_code

class ServiceMovementManager:
    def __init__(self, connection):
        self.conn = connection
        self.movements_manager = RepositoryMovementManager(self.conn)
        self.product_manager = RepositoryProductManager(self.conn)
        self.mov_types_manager = RepositoryMovementTypes(self.conn)
        self.balance_manager = RepositoryInventoryBalances(self.conn)
        self.generate_movement_code = generate_movement_code
    
    def update_balance(self, product_id):
        """Atualize o saldo de estoque."""
        try:
            # Atualiza a soma das quantidades do produto na tabela Movement
            updated_balance = self.movements_manager.total_product_quantity(product_id)
            
            # Verifica se existe saldo registrado para o produto
            balance_exists = self.balance_manager.search_product_balance(product_id)
           
            if not balance_exists:
                # Cria o primeiro registro de saldo
                self.balance_manager.create_balance(product_id, updated_balance)
            else:
                # Atualiza a tabela 'Balances' com o novo valor
                self.balance_manager.update_balance(product_id, updated_balance)
            logging.info(f'ServiceMovementManager: Saldo do produto {product_id} foi atualizado com sucesso.')
        except Exception as e:
            logging.error(f'ServiceMovementManager: Erro ao atualizar o saldo de estoque do produto {product_id}. Erro: {e}.')

    def register_movement(self, movement_obj):
        """Registra uma nova movimentação de inventário."""
        movement_code = generate_movement_code(self.movements_manager.list()) # Gera o código do movimento
        
        # Extrai os atributos do objeto de movimentação
        product_id = self.product_manager.get_product_id(movement_obj.product_code)
        quantity = movement_obj.quantity
        type_id = self.mov_types_manager.get_movement_id(movement_obj.movement_type)
        invoice = movement_obj.invoice
    
        # Verifica se os dados obrigatórios estão presentes
        if not movement_code or not product_id or not quantity or not type_id:
            logging.warning('ServiceMovementManager: Dados insuficientes para registrar movimentação.')  
            return None
        
        # Chama o método 'create' para cadastrar a movimentação
        success = self.movements_manager.create(movement_code, product_id, quantity, type_id, invoice)
        if success:
            logging.info(f'ServiceMovementManager: Movimentação de estoque "{movement_code}" registrada com sucesso.')
            # Atualiza o saldo do produto
            self.update_balance(product_id)
        else:
            logging.error(f'ServiceMovementManager: Erro ao registrar movimentação de estoque "{movement_code}".')

        return success

    def update_movement(self, movement_code, field, new_value):
        """Atualiza um campo específico de uma movimentação do estoque."""
        valid_fields = ['Product_Code', 'Quantity', 'Type', 'Invoice']
        new_product_id = None  # Inicializa new_product_id

        try:
            movement_id = self.movements_manager.get_movement_id(movement_code)
            
            if field not in valid_fields:
                logging.warning(f'ServiceMovementManager: Campo inválido: {field}. Atualização não realizada.')
                return False
            else:
                # Atualiza o campo Product_ID pelo Código do produto
                if field == 'Product_Code':
                    new_product_id = self.product_manager.get_product_id(new_value)
                    success = self.movements_manager.update(movement_id, 'Product_ID', new_product_id)
                    if success:
                        logging.info(f'ServiceMovementManager: Campo "Product_ID" da movimentação "{movement_code}" atualizado com sucesso.')
                # Atualiza o campo Type_ID pelo tipo de movimento.
                elif field == 'Type':
                    type_id = self.mov_types_manager.get_movement_id(new_value)
                    success = self.movements_manager.update(movement_id, 'Type_ID', type_id)
                    if success:
                        logging.info(f'ServiceMovementManager: Campo "Type_ID" da movimentação "{movement_code}" atualizado com sucesso.')
                # Atualiza os demais campos
                else:
                    success = self.movements_manager.update(movement_id, field, new_value)
                    if success:
                        logging.info(f'ServiceMovementManager: Campo "{field}" da movimentação "{movement_code}" atualizado com sucesso.')
                        if field == 'Quantity' and new_product_id is not None:
                            # Atualiza o saldo do produto
                            self.update_balance(new_product_id)
                    else:
                        logging.warning(f'ServiceMovementManager: Campo "{field}" da movimentação "{movement_code}" não foi atualizado.')
        except Exception as e:
            logging.error(f'ServiceMovementManager: Erro ao atualizar movimentação de estoque "{movement_code}". Erro: {e}.')

        return success

    def delete_movement(self, movement_code):
        """Deleta uma movimentação de estoque pelo código do movimento."""
        try:
            movement_id = self.movements_manager.get_movement_id(movement_code)
            product_id = self.movements_manager.get_product_id(movement_code)
            if movement_id:
                success = self.movements_manager.delete(movement_id)
                if success:
                    logging.info(f'ServiceMovementManager: Movimentação "{movement_code}" deletada com sucesso.')
                    # Atualiza o saldo do produto
                    self.update_balance(product_id)
                else:
                    logging.info(f'ServiceMovementManager: Movimentação "{movement_code}" não deletada.')
        except Exception as e:
            logging.error(f'ServiceMovementManager: Erro ao deletar movimentação "{movement_code}". Erro: {e}.')

    def search_movement(self, term='', by=''):
        """Lista todas as movimentações ou busca por uma movimentação pelo código."""
        if by == 'code':
            movement = self.movements_manager.search_by_code(term)
            if movement:
                logging.info(f'ServiceMovementManager: Movimentação encontrada para o código "{term}".')
            else:
                logging.info(f'ServiceMovementManager: Nenhuma movimentação encontrada para o código "{term}".')
            
            return movement
        else:
            movements = self.movements_manager.list()
            if movements:
                logging.info(f'ServiceMovementManager: Total de movimentações listadas: {len(movements)}.')
            else:
                logging.info('ServiceMovementManager: Nenhuma movimentação encontrada.')
            
            return movements