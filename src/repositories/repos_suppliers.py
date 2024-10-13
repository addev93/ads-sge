class RepositorySupplierManager:
    
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create a table if not exists"""
        query = '''
        CREATE TABLE IF NOT EXISTS Supplier (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CNPJ TEXT NOT NULL UNIQUE,
            Trade_Name TEXT NOT NULL UNIQUE,
            Legal_Name TEXT NOT NULL,
            Address1 TEXT NOT NULL,
            Address2 TEXT,
            Phone1 TEXT,
            Phone2 TEXT,
            Representative TEXT
        );
        '''
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print('Tabela Supplier criada com sucesso.')
        except Exception:
            pass  # Opcional: você pode logar ou lidar com erros aqui

    def create(self, cnpj, trade_name, legal_name, address1, phone1, address2='', phone2='', representative=''):
        query = '''
            INSERT INTO Supplier (CNPJ, Trade_Name, Legal_Name, Address1, Phone1, Address2, Phone2, Representative)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        '''
        try:
            self.cursor.execute(query, (cnpj, trade_name, legal_name, address1, phone1, address2, phone2, representative))
            self.conn.commit()
            return True
        except Exception as e:
            print(f'RepositorySupplierManager: erro ao cadastrar fornecedor. Erro {e}.')
            return False

    def list(self):
        query = 'SELECT * FROM Supplier;'
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception:
            return []

    def search_by_name(self, name):
        query = 'SELECT * FROM Supplier WHERE Trade_Name = ?;'
        try:
            self.cursor.execute(query, (name,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f'RepositorySupplierManager: Erro ao pesquisar produto por nome. Erro: {e}.')
            return []

    def update(self, supplier_id, field, value):
        """Method to update a specific detail of the supplier."""
        
        valid_fields = ['CNPJ', 'Trade_Name', 'Legal_Name', 'Address1', 'Address2', 'Phone1', 'Phone2', 'Representative']
        
        if field not in valid_fields:
            return False 

        query = f'''
            UPDATE Supplier 
            SET {field} = ? 
            WHERE ID = ?;
        '''
        
        try:
            self.cursor.execute(query, (value, supplier_id))
            self.conn.commit()
            return True 
        except Exception as e:
            print(f'RepositorySupplierManager: Erro ao atualizar produto. Erro: {e}.')
            return False
        
    def delete(self, supplier_id):
        query = '''
            DELETE FROM Supplier WHERE ID = ?;
        '''
        try:
            self.cursor.execute(query, (supplier_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    def close(self):
        """Closes the database connection."""
        self.conn.close()