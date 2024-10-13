from src.repositories.repos_suppliers import RepositorySupplierManager

class ServiceSupplierManager:
    def __init__(self, connection):
        # self.db_path = db_path
        self.conn = connection # sqlite3.connect(self.db_path)
        self.supplier_repos_manager = RepositorySupplierManager(self.conn)
    
    def create_supplier(self, supplier_obj):
        """Cria um novo fornecedor."""
        cnpj = supplier_obj.cnpj
        trade_name = supplier_obj.trade_name
        legal_name = supplier_obj.legal_name
        address1 = supplier_obj.address1
        phone1 = supplier_obj.phone1
        address2 = supplier_obj.address2
        phone2 = supplier_obj.phone2
        representative = supplier_obj.representative

        try:
            if self.supplier_repos_manager.create(cnpj, trade_name, legal_name, address1, phone1, address2, phone2, representative):
                print(f'Fornecedor {trade_name} cadastrado com sucesso!')
            else:
                print(f'Falha ao cadastrar fornecedor {trade_name}.')
        except Exception:
            print('Erro ao efetuar cadastro.')
    
    def search_suppliers(self, name=''):
        """Localiza um ou mais fornecedores pelo nome."""
        try:
            if name:
                # Procurar o fornecedor pelo nome fornecido
                data = self.supplier_repos_manager.search_by_name(name)
            else:
                # Lista todos os fornecedores
                data = self.supplier_repos_manager.list()
            return data
        except Exception:
            print('Erro ao pesquisar fornecedor.')

    def edit_supplier(self, name, field, new_value):
        """Edita um campo específico do fornecedor."""
        try:
            supplier_id = self.supplier_repos_manager.search_by_name(name)[0][0]

            if supplier_id:
                if self.supplier_repos_manager.update(supplier_id, field, new_value):
                    print(f'Campo {field} do fornecedor {name} foi atualizado com sucesso.')
            else:
                print('Fornecedor não localizado.')
        except Exception:
            print(f'Erro ao atualizar fornecedor.')

    def delete_supplier(self, name):
        """Deleta um Fornecedor."""
        try:
            supplier_id = self.supplier_repos_manager.search_by_name(name)[0][0]      
            if supplier_id:
                self.supplier_repos_manager.delete(supplier_id)
                print(f'Fornecedor {name} deletado com sucesso.')
        except Exception:
            print('Erro ao deletar fornecedor.')