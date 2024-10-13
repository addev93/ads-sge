class Product:
    """Represents a product in database."""

    def __init__(self, code: str, description: str, category: str, supplier1: str, supplier2='', supplier3='', stock_address=''):
        self.code = code                    # Product code set by user
        self.description = description      # Product description set by user
        self.category_id = category         # ServiceProductManager converts category string (str) to category id (int)
        self.supplier1_id = supplier1       # ServiceProductManager converts supplier1 string (str) to supplier1 id (int)
        self.supplier2_id = supplier2       # ServiceProductManager converts supplier2 string (str) to supplier2 id (int)
        self.supplier3_id = supplier3       # ServiceProductManager converts supplier3 string (str) to supplier3 id (int)
        self.stock_address = stock_address  # Stock address set by user

    def attributes(self):
        """Returns the attributes of the product as a dictionary."""
        return vars(self)

    def __str__(self):
        """String representation of the product data."""
        return (f'Product(code="{self.code}", description="{self.description}", '
                f'category_id="{self.category_id}", supplier1_id="{self.supplier1_id}", '
                f'supplier2_id="{self.supplier2_id}", supplier3_id="{self.supplier3_id}", '
                f'address="{self.stock_address}")')