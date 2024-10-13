from src.utils.table_exists import table_exists

class RepositoryMovementManager:
    
    def __init__(self, connection):
        self.class_name = type(self).__name__
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.table_exists = self.check_table_exists()
        self.create_table()
       
    def check_table_exists(self):
        """Verifica se a tabela existe no banco de dados."""
        try:
            return table_exists(self.cursor, self.class_name, 'Movement')
        except Exception as e:
            print(f'{self.class_name}: Erro ao verificar a existência da tabela Movement. Erro: {e}.')
            return False

    def create_table(self):
        """Creates the Movement table in the database if it does not exist."""
        query = '''
        CREATE TABLE IF NOT EXISTS Movement (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Movement_Code TEXT NOT NULL,
            Product_ID INTEGER NOT NULL,
            Quantity DECIMAL NOT NULL,
            Type TEXT NOT NULL,
            Invoice TEXT,
            FOREIGN KEY (Product_ID) REFERENCES Product(ID)
        );
        '''
        try:
            self.cursor.execute(query)
            self.conn.commit()
            if not self.table_exists:
                print(f'{self.class_name}: tabela Movement criada com sucesso.')
        except Exception as e:
            print(f'{self.class_name}: erro ao criar tabela Movement. Erro: {e}.')
            return None

    def create(self, movement_code, product_id, quantity, type, invoice):
        """Cria uma nova movimentação de inventário."""
        query = '''
            INSERT INTO Movement (Movement_Code, Product_ID, Quantity, Type, Invoice)
            VALUES (?, ?, ?, ?, ?);
        '''
        try:
            self.cursor.execute(query, (movement_code, product_id, quantity, type, invoice))
            self.conn.commit()
            return True
        except Exception as e:
            print(f'{self.class_name}: Erro ao registrar o movimento de estoque {movement_code}. Erro: {e}.')
            return False

    def list(self):
        """Lista todas as movimentações de inventário."""
        query = 'SELECT * FROM Movement;'
        try:
            self.cursor.execute(query)
            Movement = self.cursor.fetchall()
            return Movement
        except Exception as e:
            print(f'{self.class_name}: Erro ao listar movimentações de estoque. Erro: {e}.')
            return []

    def search_by_code(self, movement_code):
        """Localiza uma movimentação de inventário pelo código."""
        query = 'SELECT * FROM Movement WHERE Movement_Code = ?;'
        try:
            self.cursor.execute(query, (movement_code,))
            movement = self.cursor.fetchall()
            return movement
        except Exception as e:
            print(f'{self.class_name}: Erro ao localizar movimentação com o código {movement_code}. Erro: {e}.')
            return False

    def delete(self, movement_id):
        """Removes an inventory movement by ID."""
        query = 'DELETE FROM Movement WHERE ID = ?;'
        try:
            self.cursor.execute(query, (movement_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f'{self.class_name}: Erro ao deletar movimentação com ID {movement_id}. Erro: {e}.')
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
            print(f'{self.class_name}: Erro ao atualizar movimentação com ID {movement_id}. Erro: {e}.')
            return False

    def last_movement_id(self):
        """Retorna o ID da última movimentação"""
        query = 'SELECT MAX(ID) FROM Movement;'
        try:
            self.cursor.execute(query)
            last_id = self.cursor.fetchone()[0] or 0
            return last_id
        except Exception as e:
            print(f'{self.class_name}: Erro ao recuperar o último ID de movimentação. Erro: {e}.')
            return False

    def close(self):
        """Closes the database connection."""
        self.conn.close()
        print(f'{self.class_name}: Conexão com o banco de dados fechada.')