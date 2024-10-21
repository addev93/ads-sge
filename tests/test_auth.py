import syspath
syspath.set_src_path()
import unittest
from src.models.model_user import User
from src.services.service_user_manager import ServiceUserManager
from src.auth.auth import Auth
from data.data_for_testing import DataTesting
import sqlite3
import os

class TestAuth(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes."""
        cls.db_path = 'tests/temp_users.db'  # Caminho do banco de dados de teste
        cls.conn = sqlite3.connect(cls.db_path)
        cls.user_manager = ServiceUserManager(cls.conn)
        cls.data = DataTesting()
        cls.auth = Auth(cls.user_manager)

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez após todos os testes, para limpar o banco de dados."""
        cls.conn.execute('DELETE FROM User;')  # Limpa todos os registros da tabela Movement
        cls.conn.commit()
        cls.conn.close()  # Fecha a conexão com o banco de dados
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)  # Deleta o arquivo do banco de dados

    def test_autentication(self):
        """Testa a autenticação."""
        
        user = User(name='Paul', username='paul085', email='paul@email.com', password='securepass1')
        
        self.user_manager.create_user(user)
        sucess = self.auth.authenticator('paul085', 'securepass1')

        self.assertTrue(sucess)

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestAuth('test_autentication'))

    runner = unittest.TextTestRunner()
    runner.run(test_suite)