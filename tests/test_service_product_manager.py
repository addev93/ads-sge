import syspath
syspath.set_src_path()
import unittest
from src.models.model_product import Product
from src.models.model_supplier import Supplier
from src.services.service_product_manager import ServiceProductManager
import os
import sqlite3

class TestProductServices(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes."""
        cls.db_path = 'tests/temp_products.db'  # Caminho do banco de dados de teste
        cls.conn = sqlite3.connect(cls.db_path)
        cls.service_manager = ServiceProductManager(cls.conn)  # Instancia o Gerenciador de Serviços de Produto
        cls.product_manager = cls.service_manager.product_repos_manager  # Instancia do Gerenciador de Repositorio de Produto
        cls.category_manager = cls.service_manager.category_manager
        cls.supplier_manager = cls.service_manager.supplier_manager
        cls.create_product_table(cls.product_manager)  # Cria a tabela de produtos no banco de dados
        cls.create_category_table(cls.category_manager) # Cria a tabela de categorias no banco de dados
        cls.create_supplier_table(cls.supplier_manager) # Cria a tabela de fornecedores no banco de dados

    @classmethod
    def create_product_table(cls, manager):
        """Cria a tabela Product no banco de dados, se não existir."""
        # manager.create_table()
        pass
    
    @classmethod
    def create_category_table(cls, manager):
        """Cria a tabela Category no banco de dados, se não existir."""
        # manager.repos_manager.create_table()
        pass
    
    @classmethod
    def create_supplier_table(cls, manager):
        """Cria a tabela Supplier no banco de dados, se não existir."""
        # manager.supplier_repos_manager.create_table()
        pass

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez após todos os testes, para limpar o banco de dados."""
        cls.product_manager.cursor.execute('DELETE FROM Product;')  # Limpa todos os registros da tabela Product
        cls.product_manager.conn.commit()  # Salva as mudanças
        cls.product_manager.conn.close()  # Fecha a conexão com o banco de dados
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)  # Deleta o arquivo do banco de dados

    def test_register_product(self):
        """Testa a criação de um produto através do serviço de registro."""
        # Criando e registrando fornecedor e categoria primeiro
        supplier_obj = Supplier(cnpj='12345678000195', trade_name='Fornecedor 1', 
                                legal_name='Fornecedor Legal 1', address1='Endereço 1', phone1='(85) 3298-7545')
        product_obj = Product('Produto A', 'Descrição do Produto A', 'Categoria A', 'Fornecedor 1')
        
        self.supplier_manager.create_supplier(supplier_obj)
        self.category_manager.register_category('Categoria A')
        
        # print(self.supplier_manager.search_suppliers())

        self.service_manager.register_product(product_obj)

        products = self.service_manager.search_product()

        self.assertEqual(len(products), 1)  # Verifica se há um produto registrado
        self.assertEqual(products[0][1], 'Produto A')  # Verifica se o nome do produto é correto
        self.assertEqual(products[0][3], 1)  # Verifica o ID da Categoria
        self.assertEqual(products[0][4], 1)  # Verifica o ID do Fornecedor 1

    def test_edit_product_service(self):
        """Testa a edição de um produto existente."""
        supplier_obj = Supplier(cnpj='12345678000196', trade_name='Fornecedor 2', 
                                legal_name='Fornecedor Legal 2', address1='Endereço 2', phone1='(85) 1234-5678')
        product_obj = Product('Produto B', 'Descrição do Produto B', 'Categoria B', 'Fornecedor 2')
        
        self.supplier_manager.create_supplier(supplier_obj)
        self.category_manager.register_category('Categoria B')
        self.service_manager.register_product(product_obj)

        self.service_manager.edit_product('Produto B', 'Description', 'Produto B Atualizado')

        product_data = self.service_manager.search_product('Produto B Atualizado', by='desc')
        self.assertEqual(len(product_data), 1)  # Verifica se a pesquisa retornou o produto
        self.assertEqual(product_data[0][2], 'Produto B Atualizado')  # Verifica se o nome foi atualizado corretamente

    def test_delete_product_service(self):
        """Testa a exclusão de um produto existente."""
        supplier_obj = Supplier(cnpj='12345678000197', trade_name='Fornecedor 3', 
                                legal_name='Fornecedor Legal 3', address1='Endereço 3', phone1='(85) 9876-5432')
        product_obj = Product('Produto C', 'Descrição do Produto C', 'Categoria C', 'Fornecedor 3')
        
        self.supplier_manager.create_supplier(supplier_obj)
        self.category_manager.register_category('Categoria C')
        self.service_manager.register_product(product_obj)

        self.service_manager.delete_product('Produto C')

        products = self.service_manager.search_product()
        self.assertEqual(len(products), 2)  # Verifica se há dois produtos registrados

    def test_search_by_code(self):
        """Testa a busca por código do produto."""
        supplier_obj = Supplier(cnpj='12345678000198', trade_name='Fornecedor 4', 
                                legal_name='Fornecedor Legal 4', address1='Endereço 4', phone1='(85) 1111-2222')
        
        product_obj = Product('Produto D', 'Descrição do Produto D', 'Categoria D', 'Fornecedor 4')
        
        self.supplier_manager.create_supplier(supplier_obj)
        self.category_manager.register_category('Categoria D')
        self.service_manager.register_product(product_obj)

        result = self.service_manager.search_product(term='Produto D', by='code')  
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Produto D')  # Verifica se o nome do produto é correto

    def test_search_by_description(self):
        """Testa a busca por descrição do produto."""
        supplier_obj = Supplier(cnpj='12345678000199', trade_name='Fornecedor 5', 
                                legal_name='Fornecedor Legal 5', address1='Endereço 5', phone1='(85) 3333-4444')
        
        product_obj = Product('Produto E', 'Descrição do Produto E', 'Categoria E', 'Fornecedor 5')

        self.supplier_manager.create_supplier(supplier_obj)
        self.category_manager.register_category('Categoria E')
        self.service_manager.register_product(product_obj)

        result = self.service_manager.search_product(term='Descrição do Produto E', by='desc')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Produto E')  # Verifica se o nome do produto é correto

    def test_search_without_criteria(self):
        """Testa a busca sem critérios (lista todos os produtos)."""
        supplier_obj = Supplier(cnpj='12345678000185', trade_name='Fornecedor 6', 
                                legal_name='Fornecedor Legal 6', address1='Endereço 6', phone1='(85) 5555-6666')
        
        product_obj = Product('Produto F', 'Descrição do Produto F', 'Categoria F', 'Fornecedor 6')

        self.supplier_manager.create_supplier(supplier_obj)
        self.category_manager.register_category('Categoria F')
        self.service_manager.register_product(product_obj)

        result = self.service_manager.search_product()
        self.assertIn((1, 'Produto A', 'Descrição do Produto A', 1, 1, None, None, ''), result)
        self.assertIn((2, 'Produto B', 'Produto B Atualizado', 2, 2, None, None, ''), result)
        self.assertIn((4, 'Produto D', 'Descrição do Produto D', 4, 4, None, None, ''), result)
        self.assertIn((5, 'Produto E', 'Descrição do Produto E', 5, 5, None, None, ''), result)
        self.assertIn((6, 'Produto F', 'Descrição do Produto F', 6, 6, None, None, ''), result)

if __name__ == '__main__':
    # Cria uma lista de testes na ordem desejada
    suite = unittest.TestSuite()
    suite.addTest(TestProductServices('test_register_product'))
    suite.addTest(TestProductServices('test_edit_product_service'))
    suite.addTest(TestProductServices('test_delete_product_service'))
    suite.addTest(TestProductServices('test_search_by_code'))
    suite.addTest(TestProductServices('test_search_by_description'))
    suite.addTest(TestProductServices('test_search_without_criteria'))

    runner = unittest.TextTestRunner()
    runner.run(suite)