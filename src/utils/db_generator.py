from utils.db_path import get_db_path
import sqlite3

def db_generator():
    """Cria um banco de dados Sqlite"""
    db_path = get_db_path()

    # Conecta ou cria o banco de dados
    conn = sqlite3.connect(db_path)

    # Cria objeto cursor
    cursor = conn.cursor()

    # Cria tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Username TEXT NOT NULL UNIQUE,
        Email TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Category (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL UNIQUE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Supplier (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CNPJ TEXT NOT NULL UNIQUE,
        Trade_Name TEXT NOT NULL,
        Legal_Name TEXT NOT NULL,
        Address1 TEXT NOT NULL,
        Address2 TEXT,
        Phone1 TEXT,
        Phone2 TEXT,
        Representative TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Code TEXT NOT NULL,
        Description TEXT,
        Category_ID INTEGER,
        Supplier1_ID INTEGER,
        Supplier2_ID INTEGER,
        Supplier3_ID INTEGER,
        Stock_Location TEXT,
        Balance DECIMAL,
        FOREIGN KEY (Category_ID) REFERENCES Category(ID),
        FOREIGN KEY (Supplier1_ID) REFERENCES Supplier(ID),
        FOREIGN KEY (Supplier2_ID) REFERENCES Supplier(ID),
        FOREIGN KEY (Supplier3_ID) REFERENCES Supplier(ID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE Movement_Types (
        ID INT PRIMARY KEY AUTO_INCREMENT,
        Type VARCHAR(50) NOT NULL,
        Description TEXT
    );

    INSERT INTO Movement_Types (Type, Description) VALUES
    ('stockIn', 'Goods received into inventory'),
    ('stockOut', 'Goods issued out of inventory'),
    ('adjustment', 'Adjustments made to inventory due to losses or errors'),
    ('return', 'Products returned to inventory');
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Movements (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Product_ID INTEGER NOT NULL,
        Quantity DECIMAL NOT NULL,
        Type_ID TEXT NOT NULL,
        Invoice TEXT,
        FOREIGN KEY (Product_ID) REFERENCES Product(ID)
        FOREIGN KEY (Type_ID) REFERENCES Movement_Types(ID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PurchaseRequest (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Solicitation_Code TEXT NOT NULL,
        Product_ID INTEGER NOT NULL,
        Quantity DECIMAL NOT NULL,
        User_Requester_ID INT NOT NULL,
        User_Approver_ID INT,
        Status TEXT NOT NULL,
        FOREIGN KEY (Product_ID) REFERENCES Product(ID),
        FOREIGN KEY (User_Requester_ID) REFERENCES User(ID),
        FOREIGN KEY (User_Approver_ID) REFERENCES User(ID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Balances (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Product_ID INTEGER NOT NULL,
        Balance DECIMAL NOT NULL,
        FOREIGN KEY (Product_ID) REFERENCES Product(ID)
    );
    ''')

    # Confirma e fecha a conexão
    conn.commit()
    conn.close()