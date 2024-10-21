import syspath
syspath.set_src_path()
import unittest
from src.models.model_user import User
from src.services.service_user_manager import ServiceUserManager
from data.data_for_testing import DataTesting
import sqlite3
import os

class TestUsersServices(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes."""
        cls.db_path = 'tests/temp_users.db'  # Caminho do banco de dados de teste
        cls.conn = sqlite3.connect(cls.db_path)
        cls.user_manager = ServiceUserManager(cls.conn)
        cls.data = DataTesting()

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez após todos os testes, para limpar o banco de dados."""
        cls.conn.execute('DELETE FROM User;')  # Limpa todos os registros da tabela Movement
        cls.conn.commit()
        cls.conn.close()  # Fecha a conexão com o banco de dados
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)  # Deleta o arquivo do banco de dados
    
    def test_create_user(self):
        """Testa o registro de novos usuários."""
        for data in self.data.users:
            user = User(*data)
            self.user_manager.create_user(user)

        users = self.user_manager.search_users()
        self.assertEqual(len(users), 5) # Conta número de usuários cadastrados.
        self.assertEqual(users[0][1], 'John') # Verifica o nome do primeiro usuário.

    def test_edit_user(self):
        """Testa a edição de usuários."""
        user = User(name='João Virino', username='joao_virino', email='joao.virino@email.com', password='securepass78')
       
        self.user_manager.create_user(user)
        self.user_manager.edit_user('Name', 'João Virino', 'João Firmino')
        self.user_manager.edit_user('Username', 'joao_virino', 'joao_firmino')

        updated_user = self.user_manager.search_users('Username', 'joao_firmino', all=False)

        self.assertEqual(len(updated_user), 1) # verifica se retornou um usuário
        self.assertEqual(updated_user[0][1], 'João Firmino') # Verifica se o nome está atualizado
        self.assertEqual(updated_user[0][2], 'joao_firmino') # Verifica se o nome de usuário foi atualizado

    def test_delete_user(self):
        """Testa a exclusão de usuários."""
        users = self.user_manager.search_users()

        for user in users:
            self.user_manager.delete_user(user[2]) # Delete o usuário passando o Username

        updated_users = self.user_manager.search_users()

        self.assertEqual(len(updated_users), 0) # Verifica se todos os usuários foram deletados.

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestUsersServices('test_create_user'))
    test_suite.addTest(TestUsersServices('test_edit_user'))
    test_suite.addTest(TestUsersServices('test_delete_user'))
    
    runner = unittest.TextTestRunner()
    runner.run(test_suite)