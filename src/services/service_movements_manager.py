import logging
logging.basicConfig(level=logging.INFO)
from src.repositories.repos_movements import RepositoryMovementManager
from src.repositories.repos_movement_types import RepositoryMovementTypes
from src.services.service_product_manager import ServiceProductManager
from src.utils.movement_code_generator import generate_movement_code

class ServiceMovementManager:
    def __init__(self, connection):
        self.conn = connection
        self.movements_repos_manager = RepositoryMovementManager(self.conn)
        self.product_manager = ServiceProductManager(self.conn)
        self.generate_movement_code = generate_movement_code
        self.movement_types_mngt = RepositoryMovementTypes(self.conn)

    def get_product_id(self, product_code):
        """Obtém o ID do produto pelo código do produto."""
        product = {tuple[1]:tuple[0] for tuple in self.product_manager.search_product(term=product_code, by='code')}

        return product.get(product_code)
    
    def get_movement_type_id(self, movement_type):
        """Obtém o ID do tipo de movimento pelo nome tipo de movimento."""
        types_dict = {tuple[1]: tuple[0] for tuple in self.movement_types_mngt.list()}

        return types_dict.get(movement_type)
    
    def get_movement_id(self, movement_code):
        movement = {tuple[1]: tuple[0] for tuple in self.movements_repos_manager.search_by_code(movement_code)} 
    
        return movement.get(movement_code)
    
    def register_movement(self, movement_obj):
        """Registra uma nova movimentação de inventário."""

        # Extrai os atributos do objeto de movimentação
        movement_code = generate_movement_code(self.movements_repos_manager.list())
        quantity = movement_obj.quantity
        invoice = movement_obj.invoice
        product_id = self.get_product_id(movement_obj.product_id)
        type_id = self.get_movement_type_id(movement_obj.type_id)
        
        # Verifica se os dados obrigatórios estão presentes
        if not movement_code or not product_id or not quantity or not type:
            logging.warning('ServiceMovementManager: Dados insuficientes para registrar movimentação.')
            
            return None

        # Chama o método 'create' para cadastrar a movimentação
        success = self.movements_repos_manager.create(movement_code, product_id, quantity, type_id, invoice)
        if success:
            logging.info(f'ServiceMovementManager: Movimentação de estoque "{movement_code}" registrada com sucesso.')
        else:
            logging.error(f'ServiceMovementManager: Erro ao registrar movimentação de estoque "{movement_code}".')

        return success

    def search_movements(self, term='', by=''):
        """Lista todas as movimentações ou busca por uma movimentação pelo código."""
        if by == 'code':
            movement = self.movements_repos_manager.search_by_code(term)
            if movement:
                logging.info(f'ServiceMovementManager: Movimentação encontrada para o código "{term}".')
            else:
                logging.info(f'ServiceMovementManager: Nenhuma movimentação encontrada para o código "{term}".')
            
            return movement
        else:
            movements = self.movements_repos_manager.list()
            if movements:
                logging.info(f'ServiceMovementManager: Total de movimentações listadas: {len(movements)}.')
            else:
                logging.info('ServiceMovementManager: Nenhuma movimentação encontrada.')
            
            return movements

    def update_movement(self, movement_code, field, new_value):
        """Atualiza um campo específico de uma movimentação do estoque."""
        valid_fields = ['Product_Code', 'Quantity', 'Type', 'Invoice']
        
        try:
            movement_id = self.get_movement_id(movement_code)
            
            if field not in valid_fields:
                logging.warning(f'ServiceMovementManager: Campo inválido: {field}. Atualização não realizada.')
                return False
            else:
                if field == 'Product_Code':
                    product_id = self.get_product_id(new_value)
                    success = self.movements_repos_manager.update(movement_id, 'Product_ID', product_id)
                    if success:
                        logging.info(f'ServiceMovementManager: Campo "Product_ID" da movimentação "{movement_code}" atualizado com sucesso.')
                else:
                    success = self.movements_repos_manager.update(movement_id, field, new_value)
                    if success:
                        logging.info(f'ServiceMovementManager: Campo "{field}" da movimentação "{movement_code}" atualizado com sucesso.')
                    else:
                        logging.warning(f'ServiceMovementManager: Campo "{field}" da movimentação "{movement_code}" não foi atualizado.')
        except Exception as e:
            logging.error(f'ServiceMovementManager: Erro ao atualizar movimentação de estoque "{movement_code}". Erro: {e}.')

        return success

    def delete_movement(self, movement_code):
        """Deleta uma movimentação de estoque pelo ID."""
        try:
            movement_id = self.get_movement_id(movement_code)
            if movement_id:
                success = self.movements_repos_manager.delete(movement_id)
                if success:
                    logging.info(f'ServiceMovementManager: Movimentação "{movement_code}" deletada com sucesso.')
                else:
                    logging.info(f'ServiceMovementManager: Movimentação "{movement_code}" não deletada.')
        except Exception as e:
            print(logging.error(f'ServiceMovementManager: Erro ao deletar movimentação "{movement_code}". Erro: {e}.'))