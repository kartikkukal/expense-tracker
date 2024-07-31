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

        if ("expenses", ) not in tables:
            self.cursor.execute("CREATE TABLE expenses (ID INT PRIMARY KEY AUTO_INCREMENT, Date_Time DATETIME NOT NULL, Note VARCHAR(100) NOT NULL, Category INT REFERENCES categories(ID), Amount INT NOT NULL, Additional VARCHAR(100))")
        

    def add_expense(self, date_time, note, category, amount, additional):
        
        self.cursor.execute("INSERT INTO expenses (Date_Time, Note, Category, Amount, Additional) VALUES(%s, %s, %s, %s, %s)", (date_time, note, category, amount, additional))

        self.connection.commit()
    
    def get_expenses(self, order, range):

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
        
        self.cursor.execute("SELECT expenses.ID, expenses.Date_Time, expenses.Note, categories.Name AS Category, expenses.Amount, expenses.Additional FROM expenses, categories WHERE expenses.Category = categories.ID AND expenses.Date_Time > %s ORDER BY expenses.Date_Time " + order_string + ", expenses.ID " + order_string, (start.strftime("%Y-%m-%d %H:%M:%S"),))
        records = self.cursor.fetchall()

        return records
    
    def get_expense(self, id):

        self.cursor.execute("SELECT * FROM expenses WHERE ID=%s", (id, ))
        record = self.cursor.fetchone()

        return record
    
    def get_expense_by_category(self, id):

        self.cursor.execute("SELECT * FROM expenses WHERE category = %s", (id, ))
        records = self.cursor.fetchall()

        return records
    
    def update_expense(self, id, record):

        self.cursor.execute("UPDATE expenses SET Date_Time=%s, Note=%s, Category=%s, Amount=%s, Additional=%s WHERE ID=%s", (record[0], record[1], record[2], record[3], record[4], id))
        self.connection.commit()
    
    def create_category(self, name):
        
        self.cursor.execute("INSERT INTO categories (Name) VALUES (%s)", (name))
        self.connection.commit()
    
    def get_categories(self):
        
        self.cursor.execute("SELECT Name FROM categories ORDER BY ID")
        records = self.cursor.fetchall()

        return records
    
    def get_category_id(self, name):

        self.cursor.execute("SELECT ID FROM categories WHERE Name = %s", (name, ))
        record = self.cursor.fetchone()

        return record
    
    def category_spending(self, order = 0):

        query = "SELECT categories.Name, SUM(expenses.Amount) AS Amount FROM expenses JOIN categories ON expenses.Category = categories.ID GROUP BY categories.Name ORDER BY SUM(expenses.Amount)"
        
        if order == 0:
            query += " DESC"

        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data