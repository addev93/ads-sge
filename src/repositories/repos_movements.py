import logging
logging.basicConfig(level=logging.INFO)

class RepositoryMovementManager:
    
    def __init__(self, connection):
        self.class_name = type(self).__name__
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Cria a tabela Movement no banco de dados se não existir."""
        query = '''
        CREATE TABLE IF NOT EXISTS Movement (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Movement_Code VARCHAR(20) UNIQUE NOT NULL,
            Product_ID INTEGER NOT NULL,
            Quantity DECIMAL NOT NULL,
            Type_ID INTEGER NOT NULL,
            Invoice TEXT,
            FOREIGN KEY (Product_ID) REFERENCES Product(ID)
        );
        '''
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao criar tabela Movement. Erro: {e}.')
            return None

    def create(self, movement_code, product_id, quantity, type, invoice):
        """Cria uma nova movimentação de inventário."""
        query = '''
            INSERT INTO Movement (Movement_Code, Product_ID, Quantity, Type_ID, Invoice)
            VALUES (?, ?, ?, ?, ?);
        '''
        try:
            self.cursor.execute(query, (movement_code, product_id, quantity, type, invoice))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao registrar o movimento de estoque {movement_code}. Erro: {e}.')
            return False

    def list(self):
        """Lista todas as movimentações de inventário."""
        query = 'SELECT * FROM Movement;'
        try:
            self.cursor.execute(query)
            movement = self.cursor.fetchall()
            return movement
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao listar movimentações de estoque. Erro: {e}.')
            return []

    def search_by_code(self, movement_code):
        """Localiza uma movimentação de inventário pelo código."""
        query = 'SELECT * FROM Movement WHERE Movement_Code = ?;'
        try:
            self.cursor.execute(query, (movement_code,))
            movement = self.cursor.fetchall()
            return movement
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao localizar movimentação com o código {movement_code}. Erro: {e}.')
            return False

    def delete(self, movement_id):
        """Remove uma movimentação de inventário pelo ID."""
        query = 'DELETE FROM Movement WHERE ID = ?;'
        try:
            self.cursor.execute(query, (movement_id,))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao deletar movimentação com ID {movement_id}. Erro: {e}.')
            return False
    
    def update(self, movement_id, field, new_value):
        """Atualiza um campo específico de uma movimentação de inventário pelo ID."""
        query = f'''
            UPDATE Movement 
            SET {field} = ? 
            WHERE ID = ?;
        '''
        
        try:
            self.cursor.execute(query, (new_value, movement_id))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao atualizar movimentação com ID {movement_id}. Erro: {e}.')
            return False

    def last_movement_id(self):
        """Retorna o ID da última movimentação."""
        query = 'SELECT MAX(ID) FROM Movement;'
        try:
            self.cursor.execute(query)
            last_id = self.cursor.fetchone()[0] or 0
            return last_id
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao recuperar o último ID de movimentação. Erro: {e}.')
            return False
        
    def total_product_quantity(self, product_id):
        """Retorna o total da soma das quantidades das movimentações para o ID do produto."""
        query = '''
        SELECT SUM(CASE 
                        WHEN Type_ID = 2 THEN -Quantity 
                        ELSE Quantity 
                    END) 
        FROM Movement 
        WHERE Product_ID = ?;
        '''
        try:
            self.cursor.execute(query, (product_id,))
            result = self.cursor.fetchone()
            return result[0] or 0
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao atualizar o saldo do produto com ID {product_id}. Erro: {e}.')
            return None
        
    def get_movement_id(self, movement_code):
        """Retorna o ID da movimentação."""
        query = '''
        SELECT ID FROM Movement WHERE Movement_Code = ?
        '''
        try:
            self.cursor.execute(query, (movement_code,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao buscar ID da movimentação {movement_code}. Erro: {e}.')
            return None

    def get_product_id(self, movement_code):
        """Retorna o ID do Produto associado ao código da movimentação fornecido."""
        query = '''
        SELECT Product_ID FROM Movement WHERE Movement_Code = ?
        '''
        try:
            self.cursor.execute(query, (movement_code,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao buscar ID do produto da movimentação {movement_code}. Erro: {e}.')
            return None

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()
        logging.info(f'{self.class_name}: Conexão com o banco de dados fechada.')