import logging
logging.basicConfig(level=logging.INFO)

class RepositoryProductManager:
    
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Cria a tabela Product no banco de dados, se não existir."""
        query = '''
        CREATE TABLE IF NOT EXISTS Product (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Code VARCHAR(20) UNIQUE NOT NULL,
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
        except Exception as e:
            logging.error(f'RepositoryProductManager: Erro ao criar tabela Product. Erro: {e}')
            return None

    def create(self, code, description, category_id, supplier1_id, supplier2_id=None, supplier3_id=None, stock_location=''):
        """Método para registrar um novo produto no banco de dados."""
        query = '''
            INSERT INTO Product (Code, Description, Category_ID, Supplier1_ID, Supplier2_ID, Supplier3_ID, Stock_Location) 
            VALUES (?, ?, ?, ?, ?, ?, ?);
        '''
        try:
            self.cursor.execute(query, (code, description, category_id, supplier1_id, supplier2_id, supplier3_id, stock_location))
            self.conn.commit()
        except Exception as e:
            logging.error(f'RepositoryProductManager: Erro ao cadastrar produto {code}. Erro: {e}')
            return False
        return True

    def list(self):
        """Método para listar todos os produtos."""
        query = 'SELECT * FROM Product;'
        try:
            self.cursor.execute(query)
            products = self.cursor.fetchall()
            return products
        except Exception as e:
            logging.error(f'RepositoryProductManager: Erro ao listar produtos. Erro: {e}')
            return None

    def search_by_description(self, string):
        """Método para localizar produtos pela descrição."""
        query = '''
            SELECT * FROM Product WHERE Description LIKE ?
        '''
        try:
            self.cursor.execute(query, ('%' + string + '%',))
            products = self.cursor.fetchall()
            return products
        except Exception as e:
            logging.error(f'RepositoryProductManager: Erro ao localizar produto por descrição. Erro: {e}.')
            return None

    def search_by_code(self, code):
        """Retorna os dados de um produto no banco de dados pelo código do produto."""
        query = '''
            SELECT * FROM Product WHERE Code = ?
        '''
        try:
            self.cursor.execute(query, (code,))
            product = self.cursor.fetchall()
            return product
        except Exception as e:
            logging.error(f'RepositoryProductManager: Erro ao localizar o produto {code}. Erro: {e}.')
            return None

    def update(self, product_id, field, new_value):
        """Método para atualizar um campo específico de um produto."""
        query = f'''
            UPDATE Product 
            SET {field} = ?
            WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (new_value, product_id))
            self.conn.commit()
        except Exception as e:
            logging.error(f'RepositoryProductManager: Erro ao atualizar o campo {field} do produto com id {product_id}. Erro: {e}.')
            return False
        return True

    def delete(self, product_id):
        """Método para deletar um produto pelo ID."""
        query = '''
            DELETE FROM Product WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (product_id,))
            self.conn.commit()
        except Exception as e:
            logging.error(f'RepositoryProductManager: Erro ao deletar produto com id {product_id}. Erro: {e}.')
            return False
        return True

    def get_product_id(self, product_code):
        """Método para retorna o ID de um produto pelo código."""
        query = '''
        SELECT ID FROM Product WHERE Code = ?;
        '''
        try:
            self.cursor.execute(query, (product_code,))
            result = self.cursor.fetchall()
            if result:
                return result[0][0]
            else:
                return None
        except Exception as e:
            logging.error(f'RepositoryProductManager: Erro ao buscar ID do produto {product_code}. Erro: {e}.')
            return None

    def close(self):
        """Método para fechar a conexão de um banco de dados."""
        self.conn.close()
        logging.info('Conexão com o banco de dados fechada.')