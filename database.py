import mysql.connector as sql

import datetime

class Database:
    def __init__(self):

        self.connection = sql.connect(host="localhost", user="main", passwd="", database="main")
        self.cursor = self.connection.cursor()

        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()

        if ("expenses", ) not in tables:
            self.cursor.execute("CREATE TABLE expenses (ID INT PRIMARY KEY AUTO_INCREMENT, Date_Time DATETIME NOT NULL, Note VARCHAR(100) NOT NULL, Wallet INT REFERENCES wallets(ID), Category INT REFERENCES categories(ID), Amount INT NOT NULL, Additional VARCHAR(100))")
        
        if ("categories", ) not in tables:
            self.cursor.execute("CREATE TABLE categories (ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(100) NOT NULL UNIQUE)")

            # Insert default categories
            default_categories = ("Rent", "Insurance", "Loan", "Interest", "Food", "Parking", "Fuel", "Transport", "Groceries", "Gifts", "Clothes", "Events", "Phone", "Internet", "Savings", "Miscellaneous")

            for category in default_categories:
                self.cursor.execute("INSERT INTO categories (Name) VALUES (%s)", (category, ))
            
            self.connection.commit()

        if ("income", ) not in tables:
            self.cursor.execute("CREATE TABLE income (ID INT PRIMARY KEY AUTO_INCREMENT, Date_Time DATETIME NOT NULL, Note VARCHAR(100) NOT NULL, Wallet INT REFERENCES wallets(ID), Amount INT NOT NULL, Additional VARCHAR(100))")
        
        if ("wallets", ) not in tables:
            self.cursor.execute("CREATE TABLE wallets (ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(100) NOT NULL UNIQUE)")

            # Insert default wallets
            default_wallets = ("Bank", "Pocket")

            for wallet in default_wallets:
                self.cursor.execute("INSERT INTO wallets (Name) VALUES (%s)", (wallet, ))
            
            self.connection.commit()

    def add_expense(self, record):
        
        self.cursor.execute("INSERT INTO expenses (Date_Time, Note, Wallet, Category, Amount, Additional) VALUES(%s, %s, %s, %s, %s, %s)", (record[0], record[1], record[2], record[3], record[4], record[5]))
        self.connection.commit()
    
    def all_expenses(self, order, range, wallet):

        query = "SELECT expenses.ID, expenses.Date_Time, expenses.Note, categories.Name AS Category, expenses.Amount, expenses.Additional FROM expenses, categories WHERE expenses.Category = categories.ID AND expenses.Date_Time > %s"

        parameters = []

        if wallet > 0:
            query += " AND expenses.Wallet = %s"
            parameters.insert(0, wallet)

        ranges = (1, 7, 31, 90, 180, 365)

        delta = datetime.timedelta(days=ranges[range])
        time = datetime.datetime.now() - delta

        parameters.insert(0, time)

        string = ""
        if order == 0:
            string = "DESC"

        query += " ORDER BY expenses.Date_Time {}, expenses.ID {}".format(string, string)
        
        self.cursor.execute(query, parameters)
        
        return self.cursor.fetchall()
    
    def get_expense_by_id(self, id):

        self.cursor.execute("SELECT * FROM expenses WHERE ID=%s", (id, ))
        return self.cursor.fetchone()
    
    def get_expense_by_category(self, name):

        self.cursor.execute("SELECT expenses.ID, expenses.Date_Time, expenses.Note, categories.Name AS Category, expenses.Amount, expenses.Additional FROM expenses JOIN categories ON expenses.Category = categories.ID WHERE categories.Name = %s ORDER BY expenses.Date_Time DESC", (name, ))
        return self.cursor.fetchall()
    
    def total_expense_by_category(self, order = 0):

        query = "SELECT categories.Name, SUM(expenses.Amount) AS Amount FROM expenses JOIN categories ON expenses.Category = categories.ID GROUP BY categories.Name ORDER BY SUM(expenses.Amount)"
        
        if order == 0:
            query += " DESC"

        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def total_expense_by_wallet(self):

        self.cursor.execute("SELECT wallets.Name, SUM(expenses.Amount) AS Amount FROM expenses JOIN wallets ON expenses.Wallet = wallets.ID GROUP BY wallets.Name ORDER BY SUM(expenses.Amount)")
        return self.cursor.fetchall()
    
    def update_expense_by_id(self, id, record):

        self.cursor.execute("UPDATE expenses SET Date_Time=%s, Note=%s, Wallet=%s, Category=%s, Amount=%s, Additional=%s WHERE ID=%s", (record[0], record[1], record[2], record[3], record[4], record[5], id))
        self.connection.commit()
    
    def delete_expense_by_id(self, id):

        self.cursor.execute("DELETE FROM expenses WHERE ID = %s", (id, ))
        self.connection.commit()
    
    def create_category(self, name):
        
        self.cursor.execute("INSERT INTO categories (Name) VALUES (%s)", (name))
        self.connection.commit()
    
    def all_categories(self):
        
        self.cursor.execute("SELECT Name FROM categories ORDER BY ID")
        return self.cursor.fetchall()
    
    def add_income(self, record):

        self.cursor.execute("INSERT INTO income (Date_Time, Note, Wallet, Amount, Additional) VALUES (%s, %s, %s, %s, %s)", (record[0], record[1], record[2], record[3], record[4]))
        self.connection.commit()
    
    def all_income(self, order):

        query = "SELECT income.ID, income.Date_Time, income.Note, wallets.Name AS Wallet, income.Amount, income.Additional FROM income, wallets WHERE income.Wallet = wallets.ID ORDER BY income.Date_Time"

        if order == 0:
            query += " DESC"
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def total_income_by_wallet(self):

        self.cursor.execute("SELECT wallets.Name, SUM(income.Amount) AS Amount FROM income JOIN wallets ON income.Wallet = wallets.ID GROUP BY wallets.Name ORDER BY SUM(income.Amount) DESC")
        return self.cursor.fetchall()
    
    def create_wallet(self, name):
        
        self.cursor.execute("INSERT INTO wallets (Name) VALUES (%s)", (name, ))
        self.connection.commit()
    
    def all_wallets(self):

        self.cursor.execute("SELECT Name FROM wallets ORDER BY ID")
        return self.cursor.fetchall()
    
    