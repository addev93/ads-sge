import logging
logging.basicConfig(level=logging.INFO)

class RepositoryInventoryBalances:

    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Cria a tabela Balances no banco de dados, se não existir."""
        query = '''
        CREATE TABLE IF NOT EXISTS Balances (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Product_ID INTEGER NOT NULL,
            Balance DECIMAL NOT NULL,
            FOREIGN KEY (Product_ID) REFERENCES Product(ID)
        );
        '''
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return bool(self.cursor.fetchone())
        except Exception as e:
            logging.error(f'RepositoryInventoryBalances: Erro ao criar a tabela Balances. Erro: {e}.')

    def create_balance(self, product_id, balance_value):
        """Registra o primeiro saldo de estoque do produto."""
        query = '''
            INSERT INTO Balances (Product_ID, Balance)
            VALUES (?, ?);
        '''
        try:
            self.cursor.execute(query, (product_id, balance_value))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f'RepositoryInventoryBalances: Erro ao registrar o saldo do produto ID {product_id}. Erro: {e}.')
            return False

    def update_balance(self, product_id, balance_value):
        """Atualiza o saldo de estoque de um produto existente."""
        query = f'''
            UPDATE Balances 
            SET Balance = ?
            WHERE Product_ID = ?;
        '''
        try:
            self.cursor.execute(query, (product_id, balance_value))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f'RepositoryInventoryBalances: Erro ao atualizar o saldo do produto com ID {product_id}. Erro: {e}.')
            return False
        
    def search_product_balance(self, product_id):
        """Retorna o saldo atual do produto se ele existir na tabela Balances."""
        query = '''
        SELECT Balance FROM Balances WHERE Product_ID = ?
        '''
        try:
            self.cursor.execute(query, (product_id,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
      
        except Exception as e:
            logging.error(f'RepositoryInventoryBalances: Erro ao buscar saldo do produto com ID {product_id}. Erro: {e}.')
            return None 
    
    def delete_balance(self, product_id):
        """Deleta um saldo de estoque."""
        query = '''
        DELETE FROM Balances WHERE Product_ID = ?;
        '''
        try:
            self.cursor.execute(query, (product_id,))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f'RepositoryInventoryBalances: Erro ao deletar o saldo de estoque do produto com ID {product_id}. Erro: {e}.')
            return False
    
    def get_balance_id(self, product_id):
        """Busca o ID do registro de saldo pelo ID do produto."""
        query='''
        SELECT ID FROM Balances WHERE Product_ID = ?;
        '''
        try:
            self.cursor.execute(query, (product_id,))
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f'RepositoryInventoryBalances: Erro ao buscar ID do registro de saldo do produto. Erro: {e}.')
    
    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()