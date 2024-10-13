class Supplier:
    """Represents a supplier in the database."""
    def __init__(self, cnpj: str = None, trade_name: str = None, legal_name: str = None,
                 address1: str = None, phone1: str = None, address2: str = None, phone2: str = None,
                 representative: str = None):
        self.cnpj = cnpj                      # CNPJ do fornecedor, único e não nulo
        self.trade_name = trade_name          # Nome fantasia do fornecedor
        self.legal_name = legal_name          # Razão social do fornecedor
        self.address1 = address1              # Endereço principal
        self.address2 = address2              # Endereço secundário (opcional)
        self.phone1 = phone1                  # Telefone principal
        self.phone2 = phone2                  # Telefone secundário (opcional)
        self.representative = representative  # Representante do fornecedor (opcional)

    def attributes(self):
        """Returns the attributes of the supplier as a dictionary."""
        return vars(self)

    def __str__(self):
        """String representation of the supplier data."""
        return (f'Supplier(CNPJ="{self.cnpj}", Trade_Name="{self.trade_name}", '
                f'Legal_Name="{self.legal_name}")')
