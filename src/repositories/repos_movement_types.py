import logging
logging.basicConfig(level=logging.INFO)

class RepositoryMovementTypes:
    
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Cria a tabela Movement_Types no banco de dados se não existir."""
        query = '''
            CREATE TABLE IF NOT EXISTS Movement_Types (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Type VARCHAR(50) NOT NULL,
                Description TEXT
            );
        '''
        query2 = ''' 
        INSERT INTO Movement_Types (Type, Description) VALUES
            ('stockIn', 'Goods received into inventory'),
            ('stockOut', 'Goods issued out of inventory'),
            ('adjustment', 'Adjustments made to inventory due to losses or errors'),
            ('return', 'Products returned to inventory');
        '''
        
        try:
            # Criar tabela
            self.cursor.execute(query)
            self.conn.commit()
            
            # Inserir dados
            self.cursor.execute(query2)
            self.conn.commit()
            
            return True
        except Exception as e:
            logging.error(f'RepositoryMovementTypes: Erro ao criar tabela Movement_Types. Erro: {e}.')
            return None
        
    def list(self):
        """Lista todas as categorias."""
        query = '''
                SELECT * FROM Movement_Types
                '''
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f'RepositoryMovementTypes: Erro ao listar tipos de movimento. Erro: {e}.')

    def get_movement_id(self, movement_type):
        """Retorna o ID do movimento."""
        query = '''
        SELECT ID FROM Movement_Types WHERE Type = ?;
        '''
        try:
            self.cursor.execute(query, (movement_type,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            logging.error(f'RepositoryMovementTypes: Erro ao buscar ID do movimento. Erro: {e}.')
            return None