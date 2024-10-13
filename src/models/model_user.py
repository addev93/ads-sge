class User:
    """Represents a user in the database."""
    
    def __init__(self, name: str = None, username: str = None, email: str = None,
                 password: str = None):
        self.name = name                      # Nome do usuário, não nulo
        self.username = username              # Nome de usuário, único e não nulo
        self.email = email                    # Email do usuário, único e não nulo
        self.password = password              # Senha do usuário, não nula

    def attributes(self):
        """Returns the attributes of the user as a dictionary."""
        return vars(self)

    def __str__(self):
        """String representation of the user data."""
        return (f'User(Name="{self.name}", Username="{self.username}", '
                f'Email="{self.email}")')