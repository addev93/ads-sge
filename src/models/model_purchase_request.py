class PurchaseRequest:
    """Represents a purchase request in the database."""
    
    def __init__(self, product_id: int = None, quantity: float = None, 
                 user_requester_id: int = None, user_approver_id: int = None, 
                 status: str = None):
        self.product_id = product_id            # ID do produto, não nulo
        self.quantity = quantity                  # Quantidade, não nula
        self.user_requester_id = user_requester_id  # ID do usuário requisitante, não nulo
        self.user_approver_id = user_approver_id    # ID do usuário aprovador (opcional)
        self.status = status                      # Status da solicitação, não nulo

    def attributes(self):
        """Returns the attributes of the purchase request as a dictionary."""
        return vars(self)

    def __str__(self):
        """String representation of the purchase request data."""
        return (f'PurchaseRequest(Product_ID={self.product_id}, Quantity={self.quantity}, '
                f'User_Requester_ID={self.user_requester_id}, User_Approver_ID={self.user_approver_id}, '
                f'Status="{self.status}")')