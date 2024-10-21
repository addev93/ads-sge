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
from src.repositories.repos_inventory_balances import RepositoryInventoryBalances
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
        cls.balance_manager = RepositoryInventoryBalances(cls.conn)
        cls.data = DataTesting()
        cls.populate_data(cls)

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez após todos os testes, para limpar o banco de dados."""
        cls.conn.execute('DELETE FROM Movement;')  # Limpa todos os registros da tabela Movement
        cls.conn.commit()
        cls.conn.close() 
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)  # Deleta o arquivo do banco de dados

    def populate_data(cls):
        """Popula os dados de teste no banco de dados."""
        
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

    def test_register_movement(self):
        """Testa o registro de uma nova movimentação."""
        
        # Cria um objeto de movimento a partir dos dados de teste
        movement_obj = Movement(*self.data.movements[0])

        # Registra a movimentação no sistema
        success = self.movement_manager.register_movement(movement_obj)
        self.assertTrue(success)  # Verifica se a movimentação foi registrada

        # Busca todas as movimentações registradas
        movements = self.movement_manager.search_movement()
        self.assertEqual(len(movements), 1)  # Verifica se há uma movimentação registrada
        
        # Obtém a data atual para verificar o código da movimentação
        now = datetime.datetime.now()
        year = now.strftime('%y')  # Últimos dois dígitos do ano
        month = now.strftime('%m')  # Mês no formato "00"
        
        # Verifica se o código da movimentação está correto
        self.assertEqual(movements[0][1], f'MOV{year}{month}000001')


    def test_search_all_movements(self):
        """Testa a busca por movimentações."""
        movements = [
            Movement(*self.data.movements[1]),
            Movement(*self.data.movements[2]),
            Movement(*self.data.movements[3]),
            Movement(*self.data.movements[4]),
            Movement(*self.data.movements[5])
        ]

        for movement in movements:
            self.movement_manager.register_movement(movement)

        # Busca todas as movimentações
        movements = self.movement_manager.search_movement()
        self.assertEqual(len(movements), 6)  # Verifica se 6 movimentações foram registradas


    def test_search_movement_by_code(self):
        """Testa a busca de um movimento por código."""
        movement = Movement(*self.data.movements[6])
        self.movement_manager.register_movement(movement)

        now = datetime.datetime.now()
        year = now.strftime('%y')
        month = now.strftime('%m')

        # Busca o movimento pelo código
        result = self.movement_manager.search_movement(term=f'MOV{year}{month}000007', by='code')

        self.assertEqual(len(result), 1)  # Verifica se retornou um movimento
        self.assertEqual(result[0][3], 10)  # Verifica a quantidade do movimento

    def test_update_movement(self):
        """Testa a atualização de uma movimentação existente."""
        movement_obj = Movement(*self.data.movements[7])
        self.movement_manager.register_movement(movement_obj)

        now = datetime.datetime.now()
        year = now.strftime('%y')
        month = now.strftime('%m')

        # Atualiza a quantidade da movimentação
        self.movement_manager.update_movement(f'MOV{year}{month}000008', 'Quantity', 20)
        updated_movement = self.movement_manager.search_movement(term=f'MOV{year}{month}000008', by='code')
        self.assertEqual(updated_movement[0][3], 20)

        # Atualiza o código do produto
        self.movement_manager.update_movement(f'MOV{year}{month}000001', 'Product_Code', 'P010')
        updated_movement2 = self.movement_manager.search_movement(term=f'MOV{year}{month}000001', by='code')
        self.assertEqual(updated_movement2[0][2], 10) # ID do produto código 'P010'

        # Atualiza o tipo de movimento
        self.movement_manager.update_movement(f'MOV{year}{month}000001', 'Type', 'adjustment')
        updated_movement3 = self.movement_manager.search_movement(term=f'MOV{year}{month}000001', by='code')
        self.assertEqual(updated_movement3[0][4], 3) # ID do tipo de movimento 'adjustment'

    def test_update_balance(self):
        """Testa a atualização de saldo de um produto."""
        now = datetime.datetime.now()
        year = now.strftime('%y')
        month = now.strftime('%m')

        # Cria e registra o primeiro movimento
        movement_obj = Movement(*self.data.movements[8])
        self.movement_manager.register_movement(movement_obj)

        # Obtém o ID do produto a partir do movimento registrado
        movement = self.movement_manager.search_movement(term=f'MOV{year}{month}000009', by='code')
        product_id = movement[0][2]

        # Verifica o saldo atual do produto
        current_balance = self.balance_manager.search_product_balance(product_id)
        self.assertEqual(current_balance, 7)

        # Registra um segundo movimento para o mesmo produto
        movement_obj2 = Movement(*self.data.movements[9])
        self.movement_manager.register_movement(movement_obj2)

        # Verifica o saldo atualizado
        updated_balance = self.balance_manager.search_product_balance(product_id)
        self.assertEqual(updated_balance, 5)

    def test_delete_movement(self):
        """Testa a exclusão de uma movimentação existente."""
        now = datetime.datetime.now()
        year = now.strftime('%y')
        month = now.strftime('%m')

        # Registra uma movimentação
        movement_obj = Movement(*self.data.movements[8])
        self.movement_manager.register_movement(movement_obj)

        # Deleta a movimentação registrada
        self.movement_manager.delete_movement(f'MOV{year}{month}000009')

        # Coleta todos os códigos de movimentações existentes
        movements = [movement[1] for movement in self.movement_manager.search_movement()]

        # Deleta todas as movimentações restantes
        for code in movements:
            self.movement_manager.delete_movement(code)

        # Verifica se todas as movimentações foram deletadas
        movements_updated = self.movement_manager.search_movement()
        self.assertEqual(len(movements_updated), 0)

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestMovementsServices('test_register_movement'))
    test_suite.addTest(TestMovementsServices('test_search_all_movements'))
    test_suite.addTest(TestMovementsServices('test_search_movement_by_code'))
    test_suite.addTest(TestMovementsServices('test_update_movement'))
    test_suite.addTest(TestMovementsServices('test_update_balance'))
    test_suite.addTest(TestMovementsServices('test_delete_movement'))
    
    runner = unittest.TextTestRunner()
    runner.run(test_suite)