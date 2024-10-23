import logging
logging.basicConfig(level=logging.INFO)

class RepositoryUserManager:
    
    def __init__(self,connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.class_name = self.__class__.__name__
        self.create_table()

    def create_table(self):
        """Cria a tabela User no banco de dados, se não existir."""
        query = '''
        CREATE TABLE IF NOT EXISTS User (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Username TEXT NOT NULL UNIQUE,
            Email TEXT NOT NULL UNIQUE,
            Password VARCHAR(50) NOT NULL
        );
        '''
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao criar tabela "User". Erro: {e}.')
            return False 
        
    def create(self, name, username, email, password):
        """Registra um novo usuário."""
        query = '''
            INSERT INTO User (Name, Username, Email, Password) VALUES (?, ?, ?, ?);
        '''
        try:
            self.cursor.execute(query, (name, username, email, password))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao criar usuário. Erro: {e}.')
            return False

    def list(self):
        """Lista todos os usuários"""
        query = 'SELECT Name, Username, Email FROM User;'
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao listar usuários. Erro: {e}.')
            return None
        
    def search_user(self, field, value):
        """Busca um usuário pelos campos Username, Email ou Nome."""
        query = f'SELECT * FROM User WHERE {field} = ?;'
        try:
            self.cursor.execute(query, (value,))
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao pesquisar usuário por {field}. Erro: {e}.')
            return False

    def update(self, user_id, field, new_value):
        """Atualiza um campo específico do usuário."""
        query = f'''
            UPDATE User SET {field} = ? WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (new_value, user_id))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao atualizar usuaŕio. Erro: {e}.')
            return False
    
    def delete(self, user_id):
        """Deleta um usuário."""
        query = '''
            DELETE FROM User WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (user_id,))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao deletar usuário. Erro: {e}.')
            return False

    def get_user_id(self, user_name):
        """Busca o ID do usuário pelo Username."""
        query = '''
        SELECT ID FROM User WHERE Username = ?
        '''
        try:
            self.cursor.execute(query, (user_name,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                None
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao localizar o ID do usuário. Erro: {e}.')
            return None
    
    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()