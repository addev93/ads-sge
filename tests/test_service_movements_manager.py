import syspath
syspath.set_src_path()
import unittest
from src.models.model_movement import Movement
from src.models.model_product import Product
from src.models.model_supplier import Supplier
from src.services.service_movements_manager import ServiceMovementManager
from src.services.service_product_manager import ServiceProductManager
from src.services.service_supplier_manager import ServiceSupplierManager
from src.services.service_category_manager import ServiceCategoryManager
from data.data_for_testing import DataTesting
import sqlite3
import datetime
import os

class TestMovementsServices(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes."""
        cls.db_path = 'tests/temp_movements.db'  # Caminho do banco de dados de teste
        cls.conn = sqlite3.connect(cls.db_path)
        cls.movement_manager = ServiceMovementManager(cls.conn)
        cls.supplier_manager = ServiceSupplierManager(cls.conn)
        cls.product_manager = ServiceProductManager(cls.conn)
        cls.category_manager = ServiceCategoryManager(cls.conn)
        cls.data = DataTesting()
        cls.populate_data(cls)

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez após todos os testes, para limpar o banco de dados."""
        cls.conn.execute('DELETE FROM Movement;')  # Limpa todos os registros da tabela Movement
        cls.conn.commit()
        cls.conn.close()  # Fecha a conexão com o banco de dados
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)  # Deleta o arquivo do banco de dados

    def populate_data(cls):
        """Função para popular os dados de teste no banco de dados."""

        for category in cls.data.categories():
            cls.category_manager.register_category(category)
        
        for data in cls.data.suppliers():
            obj = Supplier(*data)
            cls.supplier_manager.create_supplier(obj)

        for data in cls.data.products():
            obj = Product(*data)
            cls.product_manager.register_product(obj)
            # print(cls.product_manager.search_product())
    
    def test_register_movement(self):
        """Testa o registro de uma nova movimentação."""
        
        movement_obj = Movement(*self.data.movements()[0])
        
        success = self.movement_manager.register_movement(movement_obj)
        self.assertTrue(success)  # Verifica se a movimentação foi registrada com sucesso

        movements = self.movement_manager.search_movements()
        self.assertEqual(len(movements), 1)  # Verifica se há uma movimentação registrada
        
        now = datetime.datetime.now()
        year = now.strftime('%y')  # Últimos dois dígitos do ano
        month = now.strftime('%m')  # Mês no formato "00"
        
        self.assertEqual(movements[0][1], f'MOV{year}{month}000001')  # Verifica se o código da movimentação é correto

    def test_search_all_movements(self):
        """Testa a busca por movimentações."""
        movements = [Movement(*self.data.movements()[1]),
                    Movement(*self.data.movements()[2]),
                    Movement(*self.data.movements()[3]),
                    Movement(*self.data.movements()[4]),
                    Movement(*self.data.movements()[5])]

        for movement in movements:
            self.movement_manager.register_movement(movement)

        movements = self.movement_manager.search_movements()
        self.assertEqual(len(movements), 6)

    def test_search_movement_by_code(self):
        """Testa a busca de um movimento por código."""
        movement = Movement(*self.data.movements()[6])
        self.movement_manager.register_movement(movement)

        # Obtém o ano e mês atuais
        now = datetime.datetime.now()
        year = now.strftime('%y')  # Últimos dois dígitos do ano
        month = now.strftime('%m')  # Mês no formato "00"
        
        result = self.movement_manager.search_movements(term=f'MOV{year}{month}000007', by='code')
       
        self.assertEqual(len(result), 1) # Verifica se retornou um movimento
        self.assertEqual(result[0][3], 10) # Verifica a quantidade do movimento

    def test_update_movement(self):
        """Testa a atualização de uma movimentação existente."""
        movement_obj = Movement(*self.data.movements()[7])
        self.movement_manager.register_movement(movement_obj)

        # Obtém o ano e mês atuais
        now = datetime.datetime.now()
        year = now.strftime('%y')  # Últimos dois dígitos do ano
        month = now.strftime('%m')  # Mês no formato "00"
       
        success = self.movement_manager.update_movement(f'MOV{year}{month}000008', 'Quantity', 20)
        self.assertTrue(success)  # Verifica se a atualização foi bem-sucedida

        updated_movement = self.movement_manager.search_movements(term=f'MOV{year}{month}000008', by='code')
        self.assertEqual(updated_movement[0][3], 20)  # Verifica se a quantidade foi atualizada

        success2 = self.movement_manager.update_movement(f'MOV{year}{month}000001', 'Product_Code', 'P010')
        self.assertTrue(success2) # Verifica se código foir atualizado.

    def test_delete_movement(self):
        """Testa a exclusão de uma movimentação existente."""
        # Obtém o ano e mês atuais
        now = datetime.datetime.now()
        year = now.strftime('%y')  # Últimos dois dígitos do ano
        month = now.strftime('%m')  # Mês no formato "00"
        
        movement_obj = Movement(*self.data.movements()[8])
        self.movement_manager.register_movement(movement_obj)

        self.movement_manager.delete_movement(f'MOV{year}{month}000009')

        movements = [movement[1] for movement in self.movement_manager.search_movements()]

        for code in movements:
            self.movement_manager.delete_movement(code)

        movements_updated = self.movement_manager.search_movements()
        print(movements_updated)
        
        self.assertEqual(len(movements_updated), 0)  # Verifica se todas as movimentações foram deletadas.

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestMovementsServices('test_register_movement'))
    test_suite.addTest(TestMovementsServices('test_search_all_movements'))
    test_suite.addTest(TestMovementsServices('test_search_movement_by_code'))
    test_suite.addTest(TestMovementsServices('test_update_movement'))  # Adicionado
    test_suite.addTest(TestMovementsServices('test_delete_movement'))  # Adicionado
    
    runner = unittest.TextTestRunner()
    runner.run(test_suite)