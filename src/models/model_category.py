class Category:
    """Represents a category in the database."""
    
    def __init__(self, name=''):
        self.name = name

    def attributes(self):
        """Returns the attributes of the category as a dictionary."""
        return vars(self)
    
    def __str__(self):
        """String representation of the category data."""
        return f'Category(ID={self.category_id}, Name="{self.name}")'