class RepositoryPurchaseRequestManager:
    
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
    
    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS PurchaseRequest (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Solicitation_Code TEXT NOT NULL,
            Product_ID INTEGER NOT NULL,
            Quantity DECIMAL NOT NULL,
            User_Requester_ID INT NOT NULL,
            User_Approver_ID INT,
            Status TEXT NOT NULL,
            FOREIGN KEY (Product_ID) REFERENCES Product(ID),
            FOREIGN KEY (User_Requester_ID) REFERENCES User(ID),
            FOREIGN KEY (User_Approver_ID) REFERENCES User(ID)
        );
        '''
        self.cursor.execute(query)

    def register(self, product_id, solicitation_code, quantity, user_requester_id, user_approver_id=None, status='Pending'):
        """Creates a new purchase request."""
        query = '''
            INSERT INTO PurchaseRequest (Product_ID, Quantity, User_Requester_ID, User_Approver_ID, Status)
            VALUES (?, ?, ?, ?, ?);
        '''
        try:
            self.cursor.execute(query, (product_id, solicitation_code, quantity, user_requester_id, user_approver_id, status))
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def update(self, request_id, field, new_value):
        """Updates an existing purchase request."""
        query = f"UPDATE PurchaseRequest SET {field} = ? WHERE ID = ?;"
        try:
            self.cursor.execute(query, (new_value, request_id))
            self.conn.commit()
            return True
        except Exception:
            return False

    def locate(self, solicitation_code):
        """Finds a purchase request by Solcitation Code."""
        query = 'SELECT * FROM PurchaseRequest WHERE Solicitation_Code = ?;'
        try:
            self.cursor.execute(query, (solicitation_code,))
            request = self.cursor.fetchone()
            return request
        except Exception:
            return []

    def search_request_by_product(self, product_id):
        """Finds a purchase request by Product ID."""
        query = 'SELECT * FROM PurchaseRequest WHERE Product_ID = ?;'
        try:
            self.cursor.execute(query, (product_id,))
            request = self.cursor.fetchone()
            return request
        except Exception:
            return []

    def list(self):
        """Lists all purchase requests."""
        query = 'SELECT * FROM PurchaseRequest;'
        try:
            self.cursor.execute(query)
            requests = self.cursor.fetchall()
            return requests
        except Exception:
            return []

    def delete(self, request_id):
        """Removes a purchase request by ID."""
        query = 'DELETE FROM PurchaseRequest WHERE ID = ?;'
        try:
            self.cursor.execute(query, (request_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    def close(self):
        """Closes the database connection."""
        self.conn.close()