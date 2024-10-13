
from src.repositories.repos_products import RepositoryProductManager
from src.services.service_category_manager import ServiceCategoryManager
from src.services.service_supplier_manager import ServiceSupplierManager

class ServiceProductManager:
    def __init__(self, connection):
        self.conn = connection
        self.product_repos_manager = RepositoryProductManager(self.conn)
        self.category_manager = ServiceCategoryManager(self.conn)
        self.supplier_manager = ServiceSupplierManager(self.conn)

    def register_product(self, product_obj):
        # Cria dicionários de catergorias e fornecedores cadastrados.
        category = {tuple[1]: tuple[0] for tuple in self.category_manager.repos_manager.search_by_name(product_obj.category_id)}
        supplier1 = {tuple[2]: tuple[0] for tuple in self.supplier_manager.search_suppliers(name = product_obj.supplier1_id)}
        supplier2 = {tuple[2]: tuple[0] for tuple in self.supplier_manager.search_suppliers(name = product_obj.supplier2_id)}
        supplier3 = {tuple[2]: tuple[0] for tuple in self.supplier_manager.search_suppliers(name = product_obj.supplier3_id)}

        # Extrai os atributos do objeto Produto
        code = product_obj.code
        description = product_obj.description
        category_id = category.get(product_obj.category_id) 
        supplier1_id = supplier1.get(product_obj.supplier1_id)
        supplier2_id = supplier2.get(product_obj.supplier2_id)
        supplier3_id = supplier3.get(product_obj.supplier3_id)
        stock_address = product_obj.stock_address

        # Verifica se existe o ID da categoria e ID fornecedor 1 (são campos obrigatórios)
        if not category_id:
            print(f'ServiceProductManager: produto {code} não cadastrado: "category_id" não encontrado.')
            return None
        if not supplier1_id:
            print(f'ServiceProductManager: produto {code} não cadastrado: "supplier1_id" não encontrado.')
            return None
           
        # Chama o método 'create' para cadastrar o produto.
        try:
            self.product_repos_manager.create(code, description, category_id, supplier1_id, supplier2_id, supplier3_id, stock_address)
        except Exception as e:
            print(f'ServiceProductManager: erro ao cadastrar produto {code}. Erro: {e}.')

    def search_product(self, term='', by=''):
        try:
            if by == 'code':
                product = self.product_repos_manager.search_by_code(term)
                if not product:
                    print(f'ServiceProductManager: nenhum produto localizado para o código "{term}".')
            elif by == 'desc':
                product = self.product_repos_manager.search_by_description(term)
                if not product:
                    print(f'ServiceProductManager: nenhum produto localizado para a descrição "{term}".')
            elif not by:
                product = self.product_repos_manager.list()
                if not product:
                    print('ServiceProductManager: nenhum produto localizado.')
        except Exception as e:
            print(f'ServiceProductManager: erro ao localizar produto(s). Erro: {e}.')

        return product

    def edit_product(self, code, field, new_value):
        """Edita um campo do produto."""
        try:
            # Obtem o id do produto pelo código fornecido.
            product = self.product_repos_manager.search_by_code(code)
            if product:
                product_id = product[0][0]

            # Mapea os campos que são chaves estrangeiras e define a função para buscar o ID
            field_map = {
                    'Category': self.category_manager.search_categories,
                    'Supplier1': self.supplier_manager.search_suppliers,
                    'Supplier2': self.supplier_manager.search_suppliers,
                    'Supplier3': self.supplier_manager.search_suppliers
                }
            
            # Verifica se o campo a ser atualizado está no mapeamento
            if field in field_map:
                # Obtem os dados do campo mapeado a ser atualizado
                new_value_data = field_map[field](new_value)
                if new_value_data:
                    # Obtem o ID do novo valor do campo mapeado
                    new_value_id = new_value_data[0][0]
                    # Aplica o método 'update'
                    self.product_repos_manager.update(product_id, f'{field}_ID', new_value_id)
                    print(f'ServiceProductManager: campo {field} do produto {code} atualizado com sucesso.')
                else:
                    print(f'ServiceProductManager: campo {field} pertencente ao produto {code} não localizado.')
            
            # Aplica o método 'update' para qualquer campo que não seja chave estrangeira.
            else:
                if self.product_repos_manager.update(product_id, field, new_value):
                    print(f'ServiceProductManager: campo {field} do produto {code} atualizado com sucesso.')
                else:
                    print(f'ServiceProductManager: campo {field} do produto {code} não atualizado.')
        
        except Exception as e:
            print(f'ServiceProductManager: erro ao atualizar o campo {field} do produto {code}. Erro: {e}.')

    def delete_product(self, code):
        """Deleta um registro de produto."""
        try:
            product = self.product_repos_manager.search_by_code(code)
            
            if product: 
                product_id = product[0][0]
                self.product_repos_manager.delete(product_id)
                print(f'ServiceProductManager: produto {code} deletado com sucesso.')
            else:
                print(f'ServiceProductManager: nenhuma correspondência de produto para o código {code}.')
        except Exception as e:
            print(f'ServiceProductManager: erro ao deletar o produto {code}. Erro: {e}.')