import syspath
syspath.set_src_path()
import unittest
from src.models.model_product import Product
from src.models.model_supplier import Supplier
from src.models.model_user import User
from src.services.service_purchase_request_manager import ServicePurchaseRequest
from src.services.service_supplier_manager import ServiceSupplierManager
from src.services.service_category_manager import ServiceCategoryManager
from src.services.service_product_manager import ServiceProductManager
from src.services.service_user_manager import ServiceUserManager

from data.data_for_testing import DataTesting
import sqlite3
import datetime
import os

class TestPurchaseRequestServices(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes."""
        cls.db_path = 'tests/temp_db.db'  # Caminho do banco de dados de teste
        cls.conn = sqlite3.connect(cls.db_path)
        cls.purchase_manager = ServicePurchaseRequest(cls.conn)
        cls.supplier_manager = ServiceSupplierManager(cls.conn)
        cls.category_manager = ServiceCategoryManager(cls.conn)
        cls.product_manager = ServiceProductManager(cls.conn)
        cls.user_manager = ServiceUserManager(cls.conn)
        cls.data = DataTesting()
        cls.populate_data(cls)

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez após todos os testes, para limpar o banco de dados."""
        cls.conn.execute('DELETE FROM PurchaseRequest;')    # Limpa todos os registros da tabela PurchaseRequest
        cls.conn.commit()
        cls.conn.close() 
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)  # Deleta o arquivo do banco de dados

    def populate_data(cls):
        """Popula os dados auxiliares de teste no banco de dados."""
        # Registra as categorias no banco de dados
        for category in cls.data.categories:
            cls.category_manager.register_category(category)
        
        # Registra os fornecedores no banco de dados
        for data in cls.data.suppliers:
            obj = Supplier(*data)
            cls.supplier_manager.create_supplier(obj)

        # Registra os produtos no banco de dados
        for data in cls.data.products:
            obj = Product(*data)
            cls.product_manager.register_product(obj)
        
        for data in cls.data.users:
            obj = User(*data)
            cls.user_manager.create_user(obj)

    def test_register_purchase_request(self):
        """Testa o registro de uma solicitação de compra."""
        # Registra as solictações de compra no sistema
        for data in self.data.purchase_request:
            self.purchase_manager.create_purchase_request(*data)
        
        # Lista a solicitação de compra
        purchases = self.purchase_manager.search_purchase_request()
        
        self.assertEqual(len(purchases), 10)    # Verifica se a solicitação foi registrada
        self.assertEqual(purchases[0][2], 1)    # Verifica o ID do produto da 1º solicitação.
        
        # Obtém a data atual para verificar o código da movimentação
        now = datetime.datetime.now()
        year = now.strftime('%y')   # Últimos dois dígitos do ano
        month = now.strftime('%m')  # Mês no formato "00"
        
        # Verifica se o código da movimentação está correto
        self.assertEqual(purchases[0][1], f'PR{year}{month}000001')

    def test_search_purchase_methods(self):
        """Testa a busca da solicitação por código do produto."""
        # Busca a solicitação pelo código do produto.
        result1 = self.purchase_manager.search_purchase_request('P005', by='product')
        
        # Busca a solicitação pelo próprio código.
        result2 = self.purchase_manager.search_purchase_request('PR2410000005', by='code')
        
        # Verificações
        self.assertEqual(len(result1), 2)   # Todas as solicitações
        self.assertEqual(result1[0][2], 5)  # ID do produto
        self.assertEqual(result1[1][4], 1)  # ID da solicitação
        self.assertEqual(result2[0][1], 'PR2410000005') # Código da solicitação no resultado 2.     

    def test_erro_search_purchase(self):
        """Testa erros de busca."""
        result1 = self.purchase_manager.search_purchase_request('P011', by='product') # Produto não existente
        result2 = self.purchase_manager.search_purchase_request('PR2410000020', by='code') # Solicitação não existente
        result3 = self.purchase_manager.search_purchase_request(by='description') # Método não existente
        
        # Verificações
        self.assertEqual(result1, None)
        self.assertEqual(result2, None)
        self.assertEqual(result3, None)

    def test_update_purchase_request(self):
        """Testa a atualização de uma solicitação existente."""
        now = datetime.datetime.now()
        year = now.strftime('%y')
        month = now.strftime('%m')

        # Atualiza a quantidade
        self.purchase_manager.update_purchase_request(f'PR{year}{month}000003', 'Quantity', 20)
        updated_request = self.purchase_manager.search_purchase_request(term=f'PR{year}{month}000003', by='code')
        self.assertEqual(updated_request[0][3], 20)

        # Atualiza o código do produto
        self.purchase_manager.update_purchase_request(f'PR{year}{month}000003', 'Product_Code', 'P010')
        updated_request = self.purchase_manager.search_purchase_request(term=f'PR{year}{month}000003', by='code')
        self.assertEqual(updated_request[0][2], 10) # ID do produto código 'P010'

    def test_list_pendent_requests(self):
        """Testa a listagem de solicitações pendentes."""
        result = self.purchase_manager.list_pendent_requests()    
        self.assertEqual(len(result), 10)

    def test_approve_purchase_request(self):
        """Testa a atualização do status da solicitação de compra."""
        now = datetime.datetime.now()
        year = now.strftime('%y')
        month = now.strftime('%m')

        # Testa a aprovação
        self.purchase_manager.approve_purchase_request(f'PR{year}{month}000005', "Aprovado") 
        updated_request = self.purchase_manager.search_purchase_request(term=f'PR{year}{month}000005', by='code')
        self.assertEqual(updated_request[0][6], "AP")

        # Reverte a alteração
        self.purchase_manager.approve_purchase_request(f'PR{year}{month}000005', "Pendente")

        updated_request = self.purchase_manager.search_purchase_request(term=f'PR{year}{month}000005', by='code')
        self.assertEqual(updated_request[0][6], "P")
    
        # Testa a reprovação
        self.purchase_manager.approve_purchase_request(f'PR{year}{month}000005', "Reprovado") 
        updated_request = self.purchase_manager.search_purchase_request(term=f'PR{year}{month}000005', by='code')
        self.assertEqual(updated_request[0][6], "RP")  
    
    def test_delete_purchase(self):
        """Testa a exclusão de uma solicitação de compra existente."""
    
        # Coleta todos os códigos de movimentações existentes
        requests = [data[1] for data in self.purchase_manager.search_purchase_request()]

        # Deleta todas as movimentações restantes
        for code in requests:
            self.purchase_manager.delete_purchase_request(code)

        # Verifica se todos os registros foram deletados
        requests = [self.purchase_manager.search_purchase_request()]

        self.assertEqual(requests[0], None)

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestPurchaseRequestServices('test_register_purchase_request'))
    test_suite.addTest(TestPurchaseRequestServices('test_search_purchase_methods'))
    test_suite.addTest(TestPurchaseRequestServices('test_erro_search_purchase'))
    test_suite.addTest(TestPurchaseRequestServices('test_update_purchase_request'))
    test_suite.addTest(TestPurchaseRequestServices('test_list_pendent_requests'))
    test_suite.addTest(TestPurchaseRequestServices('test_approve_purchase_request'))
    test_suite.addTest(TestPurchaseRequestServices('test_delete_purchase'))
    
    runner = unittest.TextTestRunner()
    runner.run(test_suite)