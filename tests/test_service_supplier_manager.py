import syspath
syspath.set_src_path()
import unittest
import sqlite3
from mocks import Mocks
from src.services.service_supplier_manager import ServiceSupplierManager
import os

class TestSupplierServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes."""
        cls.db_path = 'tests/temp_suppliers.db'  # Caminho do banco de dados de teste
        cls.conn = sqlite3.connect(cls.db_path)  # Cria a conexão com o banco de dados
        cls.service_manager = ServiceSupplierManager(cls.conn)  # Instancia o Gerenciador de Serviços de Fornecedores
        cls.create_table(cls.service_manager.supplier_repos_manager)  # Cria a tabela de fornecedores no banco de dados

    @classmethod
    def create_table(cls, manager):
        """Cria a tabela Supplier no banco de dados, se não existir."""
        manager.create_table()  # Presumindo que há um método create_table no repositório

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez após todos os testes, para limpar o banco de dados."""
        cls.service_manager.supplier_repos_manager.cursor.execute('DELETE FROM Supplier;')  # Limpa todos os registros da tabela Supplier
        cls.service_manager.supplier_repos_manager.conn.commit()  # Salva as mudanças
        cls.service_manager.supplier_repos_manager.conn.close()  # Fecha a conexão com o banco de dados
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)  # Deleta o arquivo do banco de dados

    def test_create_supplier(self):
        """Testa a criação de um novo fornecedor."""
        supplier_obj = Mocks.create_mock_supplier(
            cnpj='12.345.678/0001-95',
            trade_name='Supplier A',
            legal_name='Supplier A Ltda',
            address1='Address 1',
            phone1='(11) 9999-9999',
            address2='Address 2',
            phone2='(11) 8888-8888',
            representative='Representative A'
        )

        self.service_manager.create_supplier(supplier_obj)

        suppliers = self.service_manager.search_suppliers(name='Supplier A')
        self.assertEqual(len(suppliers), 1)  # Verifica se há um fornecedor registrado
        self.assertEqual(suppliers[0][1], 'Supplier A')  # Verifica se o nome do fornecedor é correto

    def test_edit_supplier(self):
        """Testa a edição de um fornecedor existente."""
        supplier_obj = Mocks.create_mock_supplier(
            cnpj='12.345.678/0001-96',
            trade_name='Supplier B',
            legal_name='Supplier B Ltda',
            address1='Address 1',
            phone1='(11) 7777-7777',
            address2='Address 2',
            phone2='(11) 6666-6666',
            representative='Representative B'
        )

        self.service_manager.create_supplier(supplier_obj)
        self.service_manager.edit_supplier('Supplier B', 'Trade_Name', 'Supplier B Updated')

        suppliers = self.service_manager.search_suppliers(name='Supplier B Updated')
        self.assertEqual(len(suppliers), 1)  # Verifica se a pesquisa retornou o fornecedor atualizado
        self.assertEqual(suppliers[0][1], 'Supplier B Updated')  # Verifica se o nome foi atualizado corretamente

    def test_delete_supplier(self):
        """Testa a exclusão de um fornecedor existente."""
        supplier_obj = Mocks.create_mock_supplier(
            cnpj='12.345.678/0001-97',
            trade_name='Supplier C',
            legal_name='Supplier C Ltda',
            address1='Address 1',
            phone1='(11) 5555-5555',
            address2='Address 2',
            phone2='(11) 4444-4444',
            representative='Representative C'
        )

        self.service_manager.create_supplier(supplier_obj)
        self.service_manager.delete_supplier('Supplier C')

        suppliers = self.service_manager.search_suppliers()
        self.assertEqual(len(suppliers), 2)  # Verifica se há os dois fornecedores anteriores

    def test_search_by_name(self):
        """Testa a busca por nome do fornecedor."""
        supplier_obj = Mocks.create_mock_supplier(
            cnpj='12.345.678/0001-98',
            trade_name='Supplier D',
            legal_name='Supplier D Ltda',
            address1='Address 1',
            phone1='(11) 3333-3333',
            address2='Address 2',
            phone2='(11) 2222-2222',
            representative='Representative D'
        )

        self.service_manager.create_supplier(supplier_obj)

        result = self.service_manager.search_suppliers(name='Supplier D')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Supplier D')  # Verifica se o nome do fornecedor é correto

    def test_search_without_criteria(self):
        """Testa a busca sem critérios (lista todos os fornecedores)."""
        supplier_obj_1 = Mocks.create_mock_supplier(
            cnpj='12.345.678/0001-99',
            trade_name='Supplier E',
            legal_name='Supplier E Ltda',
            address1='Address 1',
            phone1='(11) 1111-1111',
            address2='Address 2',
            phone2='(11) 0000-0000',
            representative='Representative E'
        )

        supplier_obj_2 = Mocks.create_mock_supplier(
            cnpj='12.345.678/0001-00',
            trade_name='Supplier F',
            legal_name='Supplier F Ltda',
            address1='Address 1',
            phone1='(11) 0000-1111',
            address2='Address 2',
            phone2='(11) 1111-0000',
            representative='Representative F'
        )

        self.service_manager.create_supplier(supplier_obj_1)
        self.service_manager.create_supplier(supplier_obj_2)

        result = self.service_manager.search_suppliers()
        self.assertEqual(len(result), 5)  # Deve retornar todos os fornecedores criados
        self.assertIn((1, 'Supplier A', 'Supplier A Ltda', '12.345.678/0001-95', 'Address 1', '(11) 9999-9999', 'Address 2', '(11) 8888-8888', 'Representative A'), result)
        self.assertIn((2, 'Supplier B Updated', 'Supplier B Ltda', '12.345.678/0001-96', 'Address 1', '(11) 7777-7777', 'Address 2', '(11) 6666-6666', 'Representative B'), result)
        self.assertIn((4, 'Supplier D', 'Supplier D Ltda', '12.345.678/0001-98', 'Address 1', '(11) 3333-3333', 'Address 2', '(11) 2222-2222', 'Representative D'), result)
        self.assertIn((5, 'Supplier E', 'Supplier E Ltda', '12.345.678/0001-99', 'Address 1', '(11) 1111-1111', 'Address 2', '(11) 0000-0000', 'Representative E'), result)
        self.assertIn((6, 'Supplier F', 'Supplier F Ltda', '12.345.678/0001-00', 'Address 1', '(11) 0000-1111', 'Address 2', '(11) 1111-0000', 'Representative F'), result)

if __name__ == '__main__':
    # Cria uma lista de testes na ordem desejada
    suite = unittest.TestSuite()
    suite.addTest(TestSupplierServices('test_create_supplier'))
    suite.addTest(TestSupplierServices('test_edit_supplier'))
    suite.addTest(TestSupplierServices('test_delete_supplier'))
    suite.addTest(TestSupplierServices('test_search_by_name'))
    suite.addTest(TestSupplierServices('test_search_without_criteria'))

    runner = unittest.TextTestRunner()
    runner.run(suite)