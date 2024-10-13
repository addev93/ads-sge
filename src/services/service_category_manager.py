from src.repositories.repos_categories import RepositoryCategoryManager

class ServiceCategoryManager:
    def __init__(self, connection):
        self.conn = connection
        self.repos_manager = RepositoryCategoryManager(self.conn)

    def register_category(self, name):
        """Cria uma nova categoria."""
        if self.repos_manager.create(name):
            print(f'Categoria {name} cadastrada com sucesso!')

    def search_categories(self, name=''):
        """Localiza uma ou mais categorias."""
        if name:
            category = self.repos_manager.search_by_name(name)
            if category:
                return category
            else:
                print(f'ServiceCategoryManager: catergoria "{name}" não encontrada.')
                return []
        else:
            categories = self.repos_manager.list()
        return categories

    def edit_category(self, name, new_name):
        """Atualiza o nome de uma categoria existente."""
        category_id = self.repos_manager.search_by_name(name)[0][0]
        if category_id:
            self.repos_manager.update(category_id, new_name)
            print(f'Categoria {name} foi atualizada para {new_name}.')
        else:
            print(f'Categoria não localizada.')

    def delete_category(self, name):
        """Deleta uma categoria pelo ID."""
        category_id = self.repos_manager.search_by_name(name)[0][0]      
        if category_id:
            self.repos_manager.delete(category_id)
            print(f'Categoria {name} deletada com sucesso.')