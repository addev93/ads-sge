# from syspath import set_src_path
# set_src_path()
# from src.services.service_product_manager import ServiceProductManager
# from src.models.model_product import Product
# import sqlite3
import os

# manager = ServiceProductManager

def database_db_tests():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'db_tests.db')

# print(db_tests_path)
# db_path_tests = os.path.join(os.path.dirname(db_path), 'tests/db_tests.db')

# dt_path = os.path.join(os.path.dirname(db_path), 'pop-products.json')

# # Abrindo e lendo o arquivo JSON
# with open(dt_path, 'r', encoding='utf-8') as file:
#     data = json.load(file)

# for dict in data:
#     product = Product()
    
#     for key, value in dict.items():
#         setattr(product, key, (value, '',''))
    
#     manager.register_product(product)