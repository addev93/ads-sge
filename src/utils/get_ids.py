from src.repositories.repos_categories import RepositoryCategoryManager
from src.repositories.repos_suppliers import RepositorySupplierManager
from src.repositories.repos_products import RepositoryProductManager

class GetIDs:
    def __init__(self, connection):
        self.conn = connection
        self.category_manager = RepositoryCategoryManager(self.conn)
        self.supplier_manager = RepositorySupplierManager(self.conn)
        self.product_manager = RepositoryProductManager(self.conn)

    def get_categories_dict(self):
        """Retorna um dicionário de categorias cadastradas."""
        categories = self.category_manager.list()
        dict_category = {}
        if categories:
            for category in categories:
                dict_category[category[1]] = category[0]
        
        return dict_category

    def get_suppliers_dict(self):
        """Retorna um dicionário de fornecedores cadastrados."""
        suppliers = self.supplier_manager.list()
        dict_suppliers = {}
        if suppliers:
            for supplier in suppliers:
                dict_suppliers[supplier[1]] = supplier[0]
        
        return dict_suppliers
    
    def get_products_dict(self):
        """Retorna um dicionário de produtos cadastrados."""
        products = self.product_manager.list()
        dict_products = {}
        if products:
            for product in products:
                dict_products[product[1]] = product[0]
        
        return dict_products