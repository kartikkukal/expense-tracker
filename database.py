import mysql.connector as sql

import datetime
import zoneinfo

class Database:
    def __init__(self):

        self.connection = sql.connect(host="localhost", user="main", passwd="", database="main")
        self.cursor = self.connection.cursor()

        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()

        if ("expenses", ) not in tables:
            self.cursor.execute("CREATE TABLE expenses (ID INT PRIMARY KEY AUTO_INCREMENT, Date_Time DATETIME NOT NULL, Note VARCHAR(100) NOT NULL, Wallet INT REFERENCES wallets(ID), Category INT REFERENCES categories(ID), Amount INT NOT NULL, Additional VARCHAR(500))")
        
        if ("categories", ) not in tables:
            self.cursor.execute("CREATE TABLE categories (ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(100) NOT NULL UNIQUE)")

            # Insert default categories
            default_categories = ("Rent", "Insurance", "Loan", "Interest", "Food", "Parking", "Fuel", "Transport", "Groceries", "Gifts", "Clothes", "Events", "Phone", "Internet", "Savings", "Miscellaneous")

            for category in default_categories:
                self.cursor.execute("INSERT INTO categories (Name) VALUES (%s)", (category, ))
            
            self.connection.commit()

        if ("income", ) not in tables:
            self.cursor.execute("CREATE TABLE income (ID INT PRIMARY KEY AUTO_INCREMENT, Date_Time DATETIME NOT NULL, Note VARCHAR(100) NOT NULL, Wallet INT REFERENCES wallets(ID), Amount INT NOT NULL, Additional VARCHAR(500))")
        
        if ("wallets", ) not in tables:
            self.cursor.execute("CREATE TABLE wallets (ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(100) NOT NULL UNIQUE)")

            # Insert default wallets
            default_wallets = ("Bank", "Pocket")

            for wallet in default_wallets:
                self.cursor.execute("INSERT INTO wallets (Name) VALUES (%s)", (wallet, ))
            
            self.connection.commit()
        
        if ("periodicals", ) not in tables:
            self.cursor.execute("CREATE TABLE periodicals (ID INT PRIMARY KEY AUTO_INCREMENT, Note VARCHAR(100) NOT NULL, Wallet INT REFERENCES wallets(ID), Category INT REFERENCES categories(ID), Frequency INT NOT NULL, Next DATETIME NOT NULL, Till DATETIME NOT NULL, Amount INT NOT NULL, Expense BOOLEAN NOT NULL)")

    def add_expense(self, record):
        
        self.cursor.execute("INSERT INTO expenses (Date_Time, Note, Wallet, Category, Amount, Additional) VALUES(%s, %s, %s, %s, %s, %s)", (record[0], record[1], record[2], record[3], record[4], record[5]))
        self.connection.commit()
    
    def all_expenses(self, order, range, wallet):

        query = "SELECT expenses.ID, expenses.Date_Time, expenses.Note, categories.Name AS Category, expenses.Amount, expenses.Additional FROM expenses JOIN categories ON expenses.Category = categories.ID JOIN wallets ON expenses.Wallet = wallets.ID WHERE expenses.Date_Time BETWEEN %s AND %s"

        parameters = []

        if wallet != "All":
            query += " AND wallets.Name = %s"
            parameters.insert(0, wallet)

        ranges = (1, 7, 31, 91, 182, 365)

        delta = datetime.timedelta(days=ranges[range])

        parameters.insert(0, datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Kolkata")))
        parameters.insert(0, datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Kolkata")) - delta)

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

        self.cursor.execute("SELECT expenses.ID, expenses.Date_Time, expenses.Note, categories.Name AS Category, expenses.Amount, expenses.Additional FROM expenses JOIN categories ON expenses.Category = categories.ID WHERE categories.Name = %s AND expenses.Date_Time < %s ORDER BY expenses.Date_Time DESC", (name, datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Kolkata"))))
        return self.cursor.fetchall()
    
    def total_expense_by_category(self, order = 0):

        query = "SELECT categories.Name, SUM(expenses.Amount) AS Amount FROM expenses JOIN categories ON expenses.Category = categories.ID WHERE expenses.Date_Time < %s GROUP BY categories.Name ORDER BY SUM(expenses.Amount)"
        
        if order == 0:
            query += " DESC"

        self.cursor.execute(query, (datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Kolkata")), ))
        return self.cursor.fetchall()
    
    def total_expense_by_wallet(self):

        self.cursor.execute("SELECT wallets.Name, SUM(expenses.Amount) AS Amount FROM expenses JOIN wallets ON expenses.Wallet = wallets.ID WHERE expenses.Date_Time < %s GROUP BY wallets.Name ORDER BY SUM(expenses.Amount)", (datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Kolkata")), ))
        return self.cursor.fetchall()
    
    def update_expense_by_id(self, id, record):

        self.cursor.execute("UPDATE expenses SET Date_Time=%s, Note=%s, Wallet=%s, Category=%s, Amount=%s, Additional=%s WHERE ID=%s", (record[0], record[1], record[2], record[3], record[4], record[5], id))
        self.connection.commit()
    
    def delete_expense_by_id(self, id):

        self.cursor.execute("DELETE FROM expenses WHERE ID = %s", (id, ))
        self.connection.commit()
    
    def delete_expense_by_category(self, id):

        self.cursor.execute("DELETE FROM expenses WHERE category=%s", (id, ))
        self.connection.commit()

    def delete_expense_by_wallet(self, id):

        self.cursor.execute("DELETE FROM expenses WHERE wallet=%s", (id, ))
        self.connection.commit()
    
    def create_category(self, name):
        
        self.cursor.execute("INSERT INTO categories (Name) VALUES (%s)", (name, ))
        self.connection.commit()
    
    def all_categories(self):
        
        self.cursor.execute("SELECT Name FROM categories ORDER BY ID")
        return self.cursor.fetchall()
    
    def get_category_by_id(self, id):

        self.cursor.execute("SELECT Name FROM categories WHERE ID=%s", (id, ))
        return self.cursor.fetchone()
    
    def get_category_id_by_name(self, name):

        self.cursor.execute("SELECT ID FROM categories WHERE Name=%s", (name, ))
        return self.cursor.fetchone()
    
    def update_category_by_id(self, id, name):

        self.cursor.execute("UPDATE categories SET Name=%s WHERE ID=%s", (name, id))
        self.connection.commit()
    
    def delete_category_by_id(self, id):

        self.cursor.execute("DELETE FROM categories WHERE ID=%s", (id, ))
        self.connection.commit()
    
    def add_income(self, record):

        self.cursor.execute("INSERT INTO income (Date_Time, Note, Wallet, Amount, Additional) VALUES (%s, %s, %s, %s, %s)", record)
        self.connection.commit()
    
    def all_income(self, order):

        query = "SELECT income.ID, income.Date_Time, income.Note, wallets.Name AS Wallet, income.Amount, income.Additional FROM income, wallets WHERE income.Wallet = wallets.ID AND income.Date_Time < %s ORDER BY income.Date_Time {}, income.ID {}"

        if order == 0:
            query = query.format("DESC", "DESC")
        else:
            query = query.format("ASC", "ASC")
        
        self.cursor.execute(query, (datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Kolkata")), ))
        return self.cursor.fetchall()
    
    def get_income_by_id(self, id):

        self.cursor.execute("SELECT * FROM income WHERE ID = %s", (id, ))
        return self.cursor.fetchone()
    
    def update_income_by_id(self, id, record):

        self.cursor.execute("UPDATE income SET Date_Time=%s, Note=%s, Wallet=%s, Amount=%s, Additional=%s WHERE ID=%s", (record[0], record[1], record[2], record[3], record[4], id))
        self.connection.commit()
    
    def total_income_by_wallet(self):

        self.cursor.execute("SELECT wallets.Name, SUM(income.Amount) AS Amount FROM income JOIN wallets ON income.Wallet = wallets.ID WHERE income.Date_Time < %s GROUP BY wallets.Name ORDER BY SUM(income.Amount) DESC", (datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Kolkata")), ))
        return self.cursor.fetchall()
    
    def delete_income_by_id(self, id):
        
        self.cursor.execute("DELETE FROM income WHERE ID = %s", (id, ))
        self.connection.commit()

    def delete_income_by_wallet(self, id):

        self.cursor.execute("DELETE FROM income WHERE wallet=%s", (id, ))
        self.connection.commit()
    
    def create_wallet(self, name):
        
        self.cursor.execute("INSERT INTO wallets (Name) VALUES (%s)", (name, ))
        self.connection.commit()
    
    def all_wallets(self):

        self.cursor.execute("SELECT Name FROM wallets ORDER BY ID")
        return self.cursor.fetchall()
    
    def get_wallet_by_id(self, id):

        self.cursor.execute("SELECT Name FROM wallets WHERE ID=%s", (id, ))
        return self.cursor.fetchone()
    
    def get_wallet_id_by_name(self, name):

        self.cursor.execute("SELECT ID FROM wallets WHERE Name=%s", (name, ))
        return self.cursor.fetchone()
    
    def update_wallet_by_id(self, id, name):

        self.cursor.execute("UPDATE wallets SET Name=%s WHERE ID=%s", (name, id))
        self.connection.commit()
    
    def delete_wallet_by_id(self, id):

        self.cursor.execute("DELETE FROM wallets WHERE ID=%s", (id, ))
        self.connection.commit()

    def add_periodical(self, record):

        self.cursor.execute("INSERT INTO periodicals (Note, Wallet, Category, Frequency, Next, Till, Amount, Expense) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", record)
        self.connection.commit()
    
    def upcoming_periodicals(self):

        self.cursor.execute("SELECT Note, Next FROM periodicals ORDER BY Next DESC")
        return self.cursor.fetchall()
    
    def income_periodicals(self, order, wallet):

        query = "SELECT periodicals.ID, periodicals.Note, wallets.Name, periodicals.Frequency, periodicals.Next, periodicals.Till, periodicals.Amount FROM periodicals JOIN wallets ON periodicals.Wallet = wallets.ID WHERE Expense=0"

        parameters = []

        if wallet != "All":
            query += " AND wallets.Name=%s"
            parameters.append(wallet)
        
        query += " ORDER BY periodicals.Next"

        if order == 1:
            query += " DESC"
        
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()
    
    def expense_periodicals(self, order, wallet):

        query = "SELECT periodicals.ID, periodicals.Note, wallets.Name, categories.Name, periodicals.Frequency, periodicals.Next, periodicals.Till, periodicals.Amount FROM periodicals JOIN wallets ON periodicals.Wallet = wallets.ID JOIN categories ON periodicals.Category = categories.ID WHERE Expense=1"

        parameters = []

        if wallet != "All":
            query += " AND wallets.Name=%s"
            parameters.append(wallet)
        
        query += " ORDER BY periodicals.Next"

        if order == 1:
            query += " DESC"
        
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def get_periodical_by_id(self, id):
        
        self.cursor.execute("SELECT * FROM periodicals WHERE ID=%s", (id, ))
        return self.cursor.fetchone()
    
    def update_periodical_by_id(self, id, record):
        
        self.cursor.execute("UPDATE periodicals SET Note=%s, Wallet=%s, Category=%s, Frequency=%s, Next=%s, Till=%s, Amount=%s, Expense=%s WHERE ID=%s", (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], id))
        self.connection.commit()
    
    def delete_periodical_by_id(self, id):
        
        self.cursor.execute("DELETE FROM periodicals WHERE ID=%s", (id, ))
        self.connection.commit()