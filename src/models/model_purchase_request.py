class PurchaseRequest:
    """Representa um solitação de compra no banco de dados."""
    def __init__(self, solic_code: str = None, product_id: int = None, quantity: float = None,
                 user_requester_id: int = None, user_approver_id: int = None, status: str = None):
        
        self.solic_code = solic_code
        self.product_id = product_id
        self.quantity = quantity
        self.user_requester_id = user_requester_id
        self.user_approver_id = user_approver_id
        self.status = status

    def attributes(self):
        """Retorna os atributos do objeto como um dicionário."""
        return vars(self)

    def __str__(self):
        """String que representa os dados da solicitação de compra."""
        return (f'PurchaseRequest(Product_ID={self.product_id}, Quantity={self.quantity}, '
                f'User_Requester_ID={self.user_requester_id}, User_Approver_ID={self.user_approver_id}, '
                f'Status="{self.status}")')