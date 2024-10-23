import logging
logging.basicConfig(level=logging.INFO)
from src.repositories.repos_purchases import RepositoryPurchaseRequest
from src.repositories.repos_products import RepositoryProductManager
from src.repositories.repos_users import RepositoryUserManager
from src.models.model_purchase_request import PurchaseRequest
from src.utils.generic_code_generator import generate_code

class ServicePurchaseRequest:
    """Serviços para gerenciamento das solicitações de compra."""
    def __init__(self, connection):
        self.conn = connection
        self.purchase_manager = RepositoryPurchaseRequest(self.conn)
        self.product_manager = RepositoryProductManager(self.conn)
        self.user_manager = RepositoryUserManager(self.conn)

    def create_purchase_request(self, product_code, quantity, user_requester):
        """Registra uma solicitação de compra no banco de dados."""
        try:
            # Cria um objeto
            purchase = PurchaseRequest()

            # Cria uma lista de códigos existentes no banco de dados
            codes = [rows[1] for rows in self.purchase_manager.search_request(method='all', term='')]
            
            # Cria um dicionário com o valor dos atributos a serem configurados
            values = {"solic_code": generate_code(codes, 'PR'),
                    "product_id": self.product_manager.get_product_id(product_code),
                    "quantity": quantity,
                    "user_requester_id": self.user_manager.get_user_id(user_requester),
                    "status": "P"}
            
            # Atribui os valores
            for att, value in values.items():
                setattr(purchase, att, value)
            
            # Registra a solicitação de compra passando o objeto criado
            sucess = self.purchase_manager.create(purchase_object=purchase)
            if sucess:
                logging.info(f"ServicePurchaseRequest => Solicitação {values.get("solic_code")} registrada com sucesso.")
        except Exception as e:
            logging.error(f"ServicePurchaseRequest => Erro ao registrar solicitação de compra {values.get("solic_code")}: {e}.")

    def search_purchase_request(self, term: str=None, by: str='all'):
        """Localiza uma ou mais solicitações de compra."""
        valid_methods = ["product", "code", "all"]
        try:
            # Valida o método.
            if by not in valid_methods:
                logging.warning(f"ServicePurchaseRequest => Método de busca '{by}' é inválido.")
                return None
            
            # Localiza o ID do produto e atribui a 'term' se a busca for por código do produto.
            if by == 'product':
                product_id = self.product_manager.get_product_id(term)
                term=product_id

            # Realiza a busca
            result = self.purchase_manager.search_request(method=by, term=term)
            
            if result:
                return result
            else:
                if term:
                    logging.info(f"ServicePurchaseRequest => Nenhum resultado de busca por {by} para o termo {term}.")
                else:
                    logging.info(f"ServicePurchaseRequest => Não há registro de solicitações de compra.")
                    return None
        except Exception as e:
            logging.error(f"ServicePurchaseRequest => Erro ao localizar solicitação de compra: {e}.")

    def list_pendent_requests(self):
        """Lista todas as solicitações pendentes de aprovação."""
        result = self.purchase_manager.search_request(method="status", term="P")
        if result:
            logging.info(f"ServicePurchaseRequest => Há {len(result)} {"solicitação pendente" if len(result) == 1 else "solicitações pendentes"}.")
            return result
        else:
            logging.info(f"ServicePurchaseRequest => Bom trabalo! Não há solicitação(ões) pendente(s).")
            return None
    
    def update_purchase_request(self, request_code, field, new_value):
        """Atualiza um campo específico da solicitação de compra."""
        valid_fields = {"Product_Code": "Product_ID", "Quantity": "Quantity" , "Status": "Status"}
        
        try:
            # Valida o campo a ser modificado
            if field not in valid_fields:
                logging.warning(f"ServicePurchaseRequest => Campo {field} é inválido.")
                return None
            
            # Define o ID da solicitação
            purchase_request_id = self.purchase_manager.get_purchase_request_id(request_code)
            if not purchase_request_id:
                logging.warning(f"ServicePurchaseRequest => ID da solicitação de compra {request_code} não foi encontrado.")
                return None 
            
            # Define o nome do campo da tabela e converte para o ID se o campo é chave estrangeira.
            field_to_update = valid_fields.get(field)
            value_to_update = self.product_manager.get_product_id(new_value) if field_to_update == "Product_ID" else new_value
              
            # Chama o método "Update" para atualizar o campo
            sucess = self.purchase_manager.update(purchase_request_id, field_to_update, value_to_update)
            
            if sucess:
                logging.info(f"ServicePurchaseRequest => Campo {field} da solicitação {request_code} foi atualizado com sucesso para {new_value}.")
        
        except Exception as e:
            logging.error(f"ServicePurchaseRequest => Erro ao atualizar o campo {field}: {e}.")
            return None
    
    def approve_purchase_request(self, request_code, new_status):
        """Altera o status da solicitação de compra."""
        # Valida o status
        valid_status = {"Aprovado": "AP", "Reprovado": "RP", "Pendente": "P"}
        if new_status not in valid_status:
            logging.info(f"ServicePurchaseRequest => Status {new_status} inválido.")
            return None
        
        # Define o ID da solicitação. 
        request_id = self.purchase_manager.get_purchase_request_id(request_code)
        if not request_id:
            logging.info(f"ServicePurchaseRequest => Solicitação de compra não localizada {request_code} não localizada.")
            return None
        
        # Atualiza o status da solicitação 
        sucess = self.purchase_manager.update(request_id, "Status", valid_status.get(new_status))
        if sucess:
            logging.info(f"ServicePurchaseRequest => Status da solicitação {request_code} foi atualizado para {new_status}.")
            return True
    
    def delete_purchase_request(self, request_code):
        """Remove uma solicitação de compra."""
        try:
            request_id = self.purchase_manager.get_purchase_request_id(request_code)
            if not request_id:
                logging.info(f"ServicePurchaseRequest => Solicitação de compra não localizada {request_code} não localizada.")
                return None
            
            sucess = self.purchase_manager.delete(request_id)
            if sucess:
                logging.info(f"ServicePurchaseRequest => Solicitação {request_code} foi deletada com sucesso.")
        except Exception as e:
            logging.error(f"ServicePurchaseRequest => Erro ao deletar a solicitação de compra {request_code}: {e}.")
        
        return None