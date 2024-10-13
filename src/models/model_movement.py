class Movement:
    """Represents a movement in the database."""
    
    def __init__(self, product_code: str = None, quantity: float = None,
                 movement_type: str = None, invoice: str = None):
        self.product_id = product_code        # ID do produto, não nulo
        self.quantity = quantity              # Quantidade, não nula
        self.type_id = movement_type    # Tipo do movimento (entrada/saída), não nulo
        self.invoice = invoice                # Nota fiscal (opcional)

    def attributes(self):
        """Returns the attributes of the movement as a dictionary."""
        return vars(self)

    def __str__(self):
        """String representation of the movement data."""
        return (f'Product_ID={self.product_id}, '
                f'Quantity={self.quantity}, Type="{self.type_id}", Invoice="{self.invoice}")')