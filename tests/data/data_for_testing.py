class DataTesting:

    def __init__(self):
        self.suppliers = self.suppliers()
        self.categories = self.categories()
        self.products = self.products()
        self.movements = self.movements()
        self.users = self.users()

    def suppliers(self):
        """Dados de fornecedores para teste."""
        suppliers_data = [
        ("12.345.678/0001-90", "Fornecedor A", "Fornecedor A LTDA", "Rua Principal, 123, Apto 101", "1111-1111", None, "2222-2222", "João Silva"),
        ("98.765.432/0001-01", "Fornecedor B", "Fornecedor B S.A.", "Avenida Secundária, 456", "3333-3333", None, None, "Maria Oliveira"),
        ("34.567.890/0001-02", "Fornecedor C", "Fornecedor C Comércio", "Rua Terceira, 789, Sala 5", "4444-4444", None, "5555-5555", None),
        ("21.987.654/0001-03", "Fornecedor D", "Fornecedor D e Cia", "Praça Central, 101", None, "6666-6666", "7777-7777", "Carlos Pereira"),
        ("54.321.098/0001-04", "Fornecedor E", "Fornecedor E Ltda", "Alameda das Flores, 202", "Casa 10", None, "8888-8888", "Ana Santos"),
        ("11.222.333/0001-05", "Fornecedor F", "Fornecedor F Comércio", "Rua da Paz, 303, Bloco B", "9999-9999", None, None, "Fernanda Lima"),
        ("22.333.444/0001-06", "Fornecedor G", "Fornecedor G Ltda", "Avenida das Américas, 404", "1010-1010", None, "2020-2020", "Ricardo Gomes"),
        ("33.444.555/0001-07", "Fornecedor H", "Fornecedor H S.A.", "Rua das Palmeiras, 505", "2121-2121", None, None, None),
        ("44.555.666/0001-08", "Fornecedor I", "Fornecedor I e Filhos", "Estrada do Sol, 606, Casa 1", "3131-3131", None, None, "Sofia Costa"),
        ("55.666.777/0001-09", "Fornecedor J", "Fornecedor J Comércio", "Rodovia da Luz, 707", "4141-4141", None, "5151-5151", "Tiago Mendes")
        ]
        return suppliers_data
    
    def categories(self):
        """Dados de categorias para teste."""
        categories_data = [
        "Eletrônicos",
        "Roupas",
        "Alimentos",
        "Beleza e Cuidados Pessoais",
        "Casa e Jardim",
        "Esportes",
        "Livros",
        "Brinquedos",
        "Música",
        "Automóveis"
        ]
        return categories_data

    def products(self):
        """Dados de produtos para teste."""
        products_data = [
        ("P001", "Produto A", "Eletrônicos", "Fornecedor A", "", "", ""),
        ("P002", "Produto B", "Roupas", "Fornecedor B", "Fornecedor C", "", ""),
        ("P003", "Produto C", "Alimentos", "Fornecedor D", "", "", ""),
        ("P004", "Produto D", "Beleza e Cuidados Pessoais", "Fornecedor E", "Fornecedor F", "Fornecedor G", ""),
        ("P005", "Produto E", "Casa e Jardim", "Fornecedor H", "", "", ""),
        ("P006", "Produto F", "Esportes", "Fornecedor I", "", "Fornecedor J", ""),
        ("P007", "Produto G", "Livros", "Fornecedor J", "", "", ""),
        ("P008", "Produto H", "Brinquedos", "Fornecedor D", "Fornecedor I", "", "Armazém 1"),
        ("P009", "Produto I", "Música", "Fornecedor H", "", "", ""),
        ("P010", "Produto J", "Automóveis", "Fornecedor B", "", "", "Armazém 2")
        ]
        return products_data
    
    def movements(self):
        """Dados de movimentos para teste."""
        movements_data = [
        ("P001", 10, "stockIn", "INV001"),
        ("P002", 5, "stockOut", "INV002"),
        ("P003", 20, "stockIn", "INV003"),
        ("P004", 15, "stockOut", "INV004"),
        ("P005", 8, "adjustment", "INV005"),
        ("P006", 12, "stockOut", "INV006"),
        ("P007", 10, "stockIn", "INV007"),
        ("P008", 3, "return", "INV008"),
        ("P009", 7, "stockIn", "INV009"),
        ("P010", 2, "adjustment", "INV010")
        ]

        return movements_data
    
    def users(sefl):
        """Dados de usuários para teste."""
        users_data = [
        ("John", "john_doe", "john@example.com", "securepassword1"),
        ("Jane", "jane_smith", "jane@example.com", "securepassword2"),
        ("Alice", "alice_jones", "alice@example.com", "securepassword3"),
        ("Bob", "bob_brown", "bob@example.com", "securepassword4"),
        ("Charlie", "charlie_black", "charlie@example.com", "securepassword5")
        ]
        return users_data
