class User:
    """Representa um usuário no banco de dados."""
    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def attributes(self):
        """Retorna os atributos do usuário como um dicionário."""
        return vars(self)

    def __str__(self):
        """String representation of the user data."""
        return (f'User(Name="{self.name}",' 
                f'Username="{self.username}",'
                f'Email="{self.email}")')