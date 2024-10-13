class RepositoryCategoryManager:
    
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Creates the Category table in the database if it does not exist."""
        query = '''
            CREATE TABLE IF NOT EXISTS Category (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL
            );
        '''
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print('Tabela Category criada com sucesso.')
            return True
        except Exception:
            return False

    def create(self, name):
        """Method to create a new category."""
        query = '''
            INSERT INTO Category (Name) VALUES (?);
        '''
        try:
            self.cursor.execute(query, (name,))
            self.conn.commit()
            return True
        except Exception:
            return False

    def list(self):
        """Method to list all categories."""
        query = 'SELECT * FROM Category'
        try:
            self.cursor.execute(query)
            categories = self.cursor.fetchall()
            return categories
        except Exception:
            return []
    
    def search_by_name(self, name):
        """Method to search for a specific category by name."""
        query = 'SELECT * FROM Category WHERE Name = ?'
        try:
            self.cursor.execute(query, (name,))
            category = self.cursor.fetchall()
            return category
        except Exception:
            return []

    def update(self, category_id, new_name):
        """Method to update the name of the category."""
        query = '''
            UPDATE Category SET Name = ? WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (new_name, category_id))
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def delete(self, category_id):
        """Method to delete the category by ID."""
        query = '''
            DELETE FROM Category WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (category_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    def close(self):
        """Closes the database connection."""
        self.conn.close()