import syspath
syspath.set_src_path()
import sqlite3
import unittest
from src.services.service_category_manager import ServiceCategoryManager
import os

class TestCategoryServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes."""
        cls.db_path = 'tests/temp.db'  # Caminho do banco de dados de teste
        cls.conn = sqlite3.connect(cls.db_path)
        cls.service_manager = ServiceCategoryManager(cls.conn)  # Instancia o Gerenciador de Serviços de Categoria
        cls.repos_manager = cls.service_manager.repos_manager
        cls.create_table(cls.repos_manager)  # Cria a tabela de categorias no banco de dados

    @classmethod
    def create_table(cls, manager):
        """Cria a tabela Category no banco de dados, se não existir."""
        manager.create_table()

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez após todos os testes, para limpar o banco de dados."""
        cls.repos_manager.cursor.execute('DELETE FROM Category;')  # Limpa todos os registros da tabela Category
        cls.repos_manager.conn.commit()  # Salva as mudanças
        cls.repos_manager.conn.close()  # Fecha a conexão com o banco de dados
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)  # Deleta o arquivo do banco de dados

    def test_register_category(self):
        """Testa a criação de uma nova categoria através do serviço de registro."""
        self.service_manager.register_category('Electronics')

        categories = self.service_manager.search_categories(name='Electronics')
        self.assertEqual(len(categories), 1)  # Verifica se há uma categoria registrada
        self.assertEqual(categories[0][1], 'Electronics')  # Verifica se o nome da categoria é correto

    def test_edit_category_service(self):
        """Testa a edição de uma categoria existente."""
        self.service_manager.register_category('Furniture')

        self.service_manager.edit_category('Furniture', 'Home Furniture')

        categories = self.service_manager.search_categories(name='Home Furniture')
        self.assertEqual(len(categories), 1)  # Verifica se a pesquisa retornou a categoria
        self.assertEqual(categories[0][1], 'Home Furniture')  # Verifica se o nome foi atualizado corretamente

    def test_delete_category_service(self):
        """Testa a exclusão de uma categoria existente."""
        self.service_manager.register_category('Books')

        self.service_manager.delete_category('Books')

        categories = self.service_manager.search_categories()
        self.assertEqual(len(categories), 2)  # Verifica se não há categorias restantes

    def test_search_by_name(self):
        """Testa a busca por nome da categoria."""
        self.service_manager.register_category('Clothing')

        result = self.service_manager.search_categories(name='Clothing')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Clothing')  # Verifica se o nome da categoria é correto

    def test_search_without_criteria(self):
        """Testa a busca sem critérios (lista todas as categorias)."""
        self.service_manager.register_category('Toys')
        self.service_manager.register_category('Games')

        result = self.service_manager.search_categories()
        self.assertEqual(len(result), 5)  # Deve retornar todas as categorias criadas
        self.assertIn((1, 'Electronics'), result)
        self.assertIn((2, 'Home Furniture'), result)
        self.assertIn((4, 'Clothing'), result)
        self.assertIn((5, 'Toys'), result)
        self.assertIn((6, 'Games'), result)

if __name__ == '__main__':
    # Cria uma lista de testes na ordem desejada
    suite = unittest.TestSuite()
    suite.addTest(TestCategoryServices('test_register_category'))
    suite.addTest(TestCategoryServices('test_edit_category_service'))
    suite.addTest(TestCategoryServices('test_delete_category_service'))
    suite.addTest(TestCategoryServices('test_search_by_name'))
    suite.addTest(TestCategoryServices('test_search_without_criteria'))

    runner = unittest.TextTestRunner()
    runner.run(suite)