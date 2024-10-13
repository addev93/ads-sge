from src.utils.table_exists import table_exists

class RepositoryProductManager:
    
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.table_exists = table_exists(self.cursor, 'RepositoryProductManager', 'Product')
        self.create_table()
    
    def table_exists(self, table_name):
        """Verifica se a tabela existe no banco de dados."""
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        try:
            self.cursor.execute(query)
            return bool(self.cursor.fetchone())
        except Exception as e:
            print(f'RepositoryProductManager: erro ao verificar existência da tabela Product. Erro: {e}.')

    def create_table(self):
        """Creates the Product table in the database if it does not exist."""
        query = '''
        CREATE TABLE IF NOT EXISTS Product (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Code TEXT NOT NULL,
            Description TEXT,
            Category_ID INTEGER,
            Supplier1_ID INTEGER,
            Supplier2_ID INTEGER,
            Supplier3_ID INTEGER,
            Stock_Location TEXT,
            FOREIGN KEY (Category_ID) REFERENCES Category(ID),
            FOREIGN KEY (Supplier1_ID) REFERENCES Supplier(ID),
            FOREIGN KEY (Supplier2_ID) REFERENCES Supplier(ID),
            FOREIGN KEY (Supplier3_ID) REFERENCES Supplier(ID)
        );
        '''
        
        try:
            self.cursor.execute(query)
            self.conn.commit()
            if not self.table_exists:
                print('RepositoryProductManager: tabela Product criada com sucesso.')
            return True
        except Exception as e:
            print(f'RepositoryProductManager: erro ao criar tabela Product. Erro: {e}.')
            return None

    def create(self, code, description, category_id, supplier1_id, supplier2_id=None, supplier3_id=None, stock_location=''):
        """Method to create a new product."""
        query = '''
            INSERT INTO Product (Code, Description, Category_ID, Supplier1_ID, Supplier2_ID, Supplier3_ID, Stock_Location) 
            VALUES (?, ?, ?, ?, ?, ?, ?);
        '''
        try:
            self.cursor.execute(query, (code, description, category_id, supplier1_id, supplier2_id, supplier3_id, stock_location))
            self.conn.commit()
            print(f'RepositoryProductManager: produto {code} cadastrado com sucesso.')
            return True
        except Exception as e:
            print(f'RepositoryProductManager: erro ao cadastrar produto {code}. Erro: {e}.')
            return False

    def list(self):
        """Method to list all products."""
        query = 'SELECT * FROM Product;'
        try:
            self.cursor.execute(query)
            products = self.cursor.fetchall()
            return products
        except Exception as e:
            print(f'RepositoryProductManager: erro ao listar produtos. Erro: {e}')
            return None

    def search_by_description(self, string):
        """Search for products by description."""
        query = '''
            SELECT * FROM Product WHERE Description LIKE ?
        '''
        try:
            self.cursor.execute(query, ('%' + string + '%',))
            products = self.cursor.fetchall()
            return products
        except Exception as e:
            print(f'RepositoryProductManager: erro ao localizar produto por descrição. Erro: {e}.')
            return None

    def search_by_code(self, code):
        """Search for a product by code."""
        query = '''
            SELECT * FROM Product WHERE Code = ?
        '''
        try:
            self.cursor.execute(query, (code,))
            product = self.cursor.fetchall()
            return product
        except Exception as e:
            print(f'RepositoryProductManager: erro ao localizar o produto {code}. Erro: {e}.')
            return None

    def update(self, product_id, field, new_value):
        """Method to update a specific product detail."""
        valid_fields = ['Code', 'Description', 'Category_ID', 'Supplier1_ID', 'Supplier2_ID', 'Supplier3_ID', 'Stock_Location']
        
        if field not in valid_fields:
            print(f'Campo {field} não é válido.')
            return False
        
        query = f'''
            UPDATE Product 
            SET {field} = ?
            WHERE ID = ?;
        '''
        
        try:
            self.cursor.execute(query, (new_value, product_id))
            self.conn.commit()
            print(f'RepositoryProductManager: o campo {field} foi atualizado para {new_value}.')
            return True
        except Exception as e:
            print(f'RepositoryProductManager: erro ao atualizar o campo {field} do produto com id {product_id}. Erro: {e}.')
            return False

    def delete(self, product_id):
        """Method to delete the product by ID."""
        query = '''
            DELETE FROM Product WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (product_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    def close(self):
        """Closes the database connection."""
        self.conn.close()