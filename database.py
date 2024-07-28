import mysql.connector as sql

import datetime

class database:
    def __init__(self):
        self.connection = sql.connect(host="localhost", user="main", passwd="", database="main")
        self.cursor = self.connection.cursor()

        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        
        if ("categories", ) not in tables:
            self.cursor.execute("CREATE TABLE categories (ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(100) NOT NULL UNIQUE)")

            default_categories = ("Rent", "Insurance", "Loan", "Interest", "Food", "Parking", "Fuel", "Transport", "Groceries", "Gifts", "Clothes", "Events", "Phone", "Internet", "Savings", "Miscellaneous")

            for category in default_categories:
                self.cursor.execute("INSERT INTO categories (Name) VALUES (%s)", (category, ))
            
            self.connection.commit()

        if ("transactions", ) not in tables:
            self.cursor.execute("CREATE TABLE transactions (ID INT PRIMARY KEY AUTO_INCREMENT, Date_Time DATETIME NOT NULL, Note VARCHAR(100) NOT NULL, Category INT REFERENCES categories(ID), Amount INT NOT NULL, Additional VARCHAR(100))")
        

    def create_transaction(self, date_time, note, category, amount, additional):
        
        self.cursor.execute("INSERT INTO transactions (Date_Time, Note, Category, Amount, Additional) VALUES(%s, %s, %s, %s, %s)", (date_time, note, category, amount, additional))

        self.connection.commit()
    
    def get_transactions(self, order, range):

        now = datetime.datetime.now()
        delta = datetime.timedelta(days=1)

        if range == 1:
            delta = datetime.timedelta(days=7)
        elif range == 2:
            delta = datetime.timedelta(days=31)
        elif range == 3:
            delta = datetime.timedelta(days=90)
        elif range == 4:
            delta = datetime.timedelta(days=180)
        elif range == 5:
            delta = datetime.timedelta(days=365)
        
        start = now - delta

        order_string = "DESC"
        
        if order == 1:
            order_string = "ASC"
        
        self.cursor.execute("SELECT transactions.ID, transactions.Date_Time, transactions.Note, categories.Name AS Category, transactions.Amount, transactions.Additional FROM transactions, categories WHERE transactions.Category = categories.ID AND transactions.Date_Time > %s ORDER BY transactions.Date_Time " + order_string + ", transactions.ID " + order_string, (start.strftime("%Y-%m-%d %H:%M:%S"),))
        records = self.cursor.fetchall()

        return records
    
    def get_transaction(self, id):

        self.cursor.execute("SELECT * FROM transactions WHERE ID=%s", (id, ))
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
    
    def category_spending(self):

        self.cursor.execute("SELECT categories.Name, SUM(transactions.Amount) AS Amount FROM transactions JOIN categories ON transactions.Category = categories.ID GROUP BY categories.Name")

        data = self.cursor.fetchall()
        
        if len(data) == 0:
            return ("No transactions", ), (1, )

        label, amount = zip(*data)

        return label, amount