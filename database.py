import mysql.connector as sql

class database:
    def __init__(self):
        self.connection = sql.connect(host="localhost", user="main", passwd="", database="main")
        self.cursor = self.connection.cursor()

        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        
        if ("categories", ) not in tables:
            self.cursor.execute("CREATE TABLE categories (ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(100)) UNIQUE NOT NULL")

            default_categories = ("Rent", "Insurance", "Loan", "Interest", "Food", "Parking", "Fuel", "Transport", "Groceries", "Gifts", "Clothes", "Events", "Phone", "Internet", "Savings", "Miscellaneous")

            for category in default_categories:
                self.cursor.execute("INSERT INTO categories (Name) VALUES (%s)", (category, ))
            
            self.connection.commit()

        if ("transactions", ) not in tables:
            self.cursor.execute("CREATE TABLE transactions (ID INT PRIMARY KEY AUTO_INCREMENT, Date_Time DATETIME NOT NULL, Note VARCHAR(100) NOT NULL, Category INT REFERENCES categories(ID)), Amount INT NOT NULL, Additional VARCHAR(100)")
        

    def create_transaction(self, date_time, note, category, amount, additional):
        
        self.cursor.execute("INSERT INTO transactions (Date_Time, Note, Category, Amount, Additional) VALUES(%s, %s, %s, %s, %s)", (date_time, note, category, amount, additional))

        self.connection.commit()
    
    def get_transactions(self, order, range):

        query = "SELECT transactions.ID, transactions.Date_Time, transactions.Note, categories.Name AS Category, transactions.Amount, transactions.Additional FROM transactions, categories WHERE transactions.Category = categories.ID ORDER BY transactions.Date_Time"
        
        if order == 0:
            query = query + " DESC"
        
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        return records
    
    def get_transaction(self, id):

        self.cursor.execute("SELECT * FROM transactions WHERE ID=%s", (id))
        record = self.cursor.fetchone()

        return record
    
    def update_transaction(self, id, record):

        self.cursor.execute("UPDATE transactions SET Date_Time=%s, Note=%s, Category=%s, Amount=%s, Additional=%s WHERE ID=%s", (record[0], record[1], record[2], record[3], record[4], id))
        self.connection.commit()
    
    def create_category(self, name):
        
        self.cursor.execute("INSERT INTO categories (Name) VALUES (%s)", (name))
        self.connection.commit()
    
    def get_categories(self):
        
        self.cursor.execute("SELECT Name FROM categories ORDER BY ID")
        records = self.cursor.fetchall()

        return records