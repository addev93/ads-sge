import logging
logging.basicConfig(level=logging.INFO)

class RepositoryPurchaseRequest:
    
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        """Cria a tabela PurchaseRequest se não existir."""
        query = '''
        CREATE TABLE IF NOT EXISTS PurchaseRequest (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Solicitation_Code TEXT UNIQUE NOT NULL,
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
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            logging.error(f"RepositoryPurchaseRequest => Erro ao criar tabela PurchaseRequest: {e}.")

    def create(self, purchase_object):
        """Registra uma nova solicitação de compra."""
        obj = purchase_object
        query = '''
            INSERT INTO PurchaseRequest (Solicitation_Code, Product_ID, Quantity, User_Requester_ID, User_Approver_ID, Status)
            VALUES (?, ?, ?, ?, ?, ?);
        '''
        try:
            self.cursor.execute(query, (obj.solic_code, obj.product_id, obj.quantity, obj.user_requester_id, obj.user_approver_id, obj.status))
            self.conn.commit()
            return True
        except Exception as e:
            logging.info(f'RepositoryPurchaseRequest => Erro ao registrar a solicitação de compra {obj.solic_code}: {e}.')
            return False
    
    def update(self, request_id, field, new_value):
        """Atualiza uma solicitação de compra existente."""
        query = f"UPDATE PurchaseRequest SET {field} = ? WHERE ID = ?;"
        try:
            self.cursor.execute(query, (new_value, request_id))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"RepositoryPurchaseRequest => Erro ao atualizar campo {field}: {e}.")
            return False

    def search_request(self, method, term):
        """Localiza uma ou mais solicitações de compra por produto, código da solicitação ou todas as solicitações."""
        
        query = {"product": "SELECT * FROM PurchaseRequest WHERE Product_ID = ?;",
                "code": "SELECT * FROM PurchaseRequest WHERE Solicitation_Code = ?;",
                "status": "SELECT * FROM PurchaseRequest WHERE Status = ?;",
                "all": "SELECT * FROM PurchaseRequest;"}
        try:
            if method=='all':
                self.cursor.execute(query.get(method))
            else:
                self.cursor.execute(query.get(method), (term,))
            result = self.cursor.fetchall()
            if result:
                return result
            else:
                return [] 
         
        except Exception as e:
            logging.error(f'RepositoryPurchaseRequest => Erro ao localizar solicitação de compra por {method}: {e}.')
            return None

    def get_purchase_request_id(self, solic_code):
        """Busca o ID da solicitação de compra."""
        query = '''
        SELECT ID FROM PurchaseRequest WHERE Solicitation_Code = ?
        '''
        try:
            self.cursor.execute(query, (solic_code,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            logging.info(f"RepositoryPurchaseRequest => Erro ao buscar ID da solicitação de compra {solic_code}: {e}.")

    def delete(self, request_id):
        """Remove uma solicitação de compra pelo ID."""
        query = 'DELETE FROM PurchaseRequest WHERE ID = ?;'
        try:
            self.cursor.execute(query, (request_id,))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"RepositoryPurchaseRequest => Erro ao deletar a solicitação ID {request_id}: {e}.")
            return False

    def close(self):
        """Fecha a conexão com o  banco de dados."""
        self.conn.close()