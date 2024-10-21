class Movement:
    """Representa um movimento de estoque na entrada de dados."""
    def __init__(self, product_code: str = None, quantity: float = None,
                 movement_type: str = None, invoice: str = None):
        self.product_code = product_code
        self.quantity = quantity
        self.movement_type = movement_type
        self.invoice = invoice

    def attributes(self):
        """Retorna os atributos do objeto movimento como um dicionário."""
        return vars(self)

    def __str__(self):
        """String que representa os atributos do movimento."""
        return (f'Product_Code="{self.product_code}",'
                f'Quantity={self.quantity}, Type="{self.movement_type}", Invoice="{self.invoice}")')