class RepositoryUserManager:
    
    def __init__(self,connection):
        self.conn = connection
        self.cursor = self.conn.cursor()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS User (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Username TEXT NOT NULL UNIQUE,
            Email TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL
        );
        '''
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception:
            pass  # Opcional: você pode logar ou lidar com erros aqui

    def create(self, name, username, email, password):
        query = '''
            INSERT INTO User (Name, Username, Email, Password) VALUES (?, ?, ?, ?);
        '''
        try:
            self.cursor.execute(query, (name, username, email, password))
            self.conn.commit()
            return True
        except Exception:
            return False

    def delete(self, user_id):
        query = '''
            DELETE FROM User WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (user_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    def list(self):
        query = 'SELECT * FROM User;'
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception:
            return []
        
    def search_user(self, user_id):
        query = 'SELECT * FROM User WHERE ID = ?;'
        try:
            self.cursor.execute(query, (user_id,))
            user = self.cursor.fetchall()
            return user
        except Exception:
            return False

    def update(self, user_id, field, new_value):
        query = f'''
            UPDATE User SET {field} = ? WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (new_value, user_id))
            self.conn.commit()
            return True
        except Exception:
            return False

    def close(self):
        """Closes the database connection."""
        self.conn.close()
