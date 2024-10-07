from tkinter import ttk
import tkinter as tk

from dateutil.relativedelta import relativedelta
import datetime

from dialogs.add_periodical_income import AddPeriodicalIncome
from dialogs.add_periodical_expense import AddPeriodicalExpense
from dialogs.view_periodical_income import ViewPeriodicalIncome
from dialogs.view_periodical_expense import ViewPeriodicalExpense

class Periodicals:
    def __init__(self, root):

        self.root = root

        # Initialize root frame
        self.frame = ttk.Frame(root.notebook, padding="5")
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(tuple(range(2)), weight=1, uniform="fred")
        self.frame.columnconfigure(0, weight=1, uniform="fred")

        # Initialize frames
        income = ttk.Frame(self.frame)
        expenses = ttk.Frame(self.frame)

        controls = ttk.Frame(income)
        controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        # Next sorting drop down
        ttk.Label(controls, text="Next: ").pack(side=tk.LEFT, padx=20)

        self.sort_options = ("Closest", "Farthest")

        self.sort_selected_income = tk.StringVar(value=self.sort_options[0])

        ttk.OptionMenu(controls, self.sort_selected_income, self.sort_options[0], *self.sort_options, command=lambda _ : self.update_periodicals()).pack(side=tk.LEFT, ipadx=8)

        # Wallet drop down
        ttk.Label(controls, text="Wallet: ").pack(side=tk.LEFT, padx=20)

        self.wallet_options = self.root.mysql.all_wallets()
        self.wallet_options = ["All"] + [value for row in self.wallet_options for value in row]

        self.wallet_select_income = tk.StringVar(value=self.wallet_options[0])

        self.wallet_widget_income = ttk.OptionMenu(controls, self.wallet_select_income, self.wallet_options[0], *self.wallet_options, command=lambda _ : self.update_periodicals())
        self.wallet_widget_income.pack(side=tk.LEFT, ipadx=8)

        self.root.wallet_update.append(self.update_income_wallets(controls))

        self.AddPeriodicalIncome = AddPeriodicalIncome(root)

        # Add income periodical button
        ttk.Button(controls, text="Add Income", style="Accent.TButton", command=self.AddPeriodicalIncome.run).pack(side=tk.RIGHT, padx=25)

        # Refresh button
        ttk.Button(controls, text="Refresh", command=self.refresh).pack(side=tk.RIGHT)

        income.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        expenses.grid(row=1, column=0, padx=5, pady=5, sticky="news")

        self.ViewPeriodicalIncome = ViewPeriodicalIncome(self.root)

        self.income = ttk.Treeview(income, columns=("note", "wallet", "frequency", "amount"))
        self.income.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.income.heading("#0", text="Next")
        self.income.column("#0", width=40)

        self.income.heading("note", text="Note")
        
        self.income.heading("wallet", text="Wallet")
        self.income.column("wallet", width=40, anchor=tk.CENTER)

        self.income.heading("frequency", text="Frequency")
        self.income.column("frequency", width=40, anchor=tk.CENTER)

        self.income.heading("amount", text="Amount")
        self.income.column("amount", width=40, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(income, orient=tk.VERTICAL, command=self.income.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.income.configure(yscrollcommand=scrollbar.set)
        self.income.bind("<Double-1>", self.income_selected)

        controls = ttk.Frame(expenses)
        controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        # Next sorting drop down
        ttk.Label(controls, text="Next: ").pack(side=tk.LEFT, padx=20)

        self.sort_selected_expenses = tk.StringVar(value=self.sort_options[0])

        ttk.OptionMenu(controls, self.sort_selected_expenses, self.sort_options[0], *self.sort_options, command=lambda _ : self.update_periodicals()).pack(side=tk.LEFT, ipadx=8)

        self.AddPeriodicalExpense = AddPeriodicalExpense(root)

        # Wallet drop down
        ttk.Label(controls, text="Wallet: ").pack(side=tk.LEFT, padx=20)

        self.wallet_select_expenses = tk.StringVar(value=self.wallet_options[0])

        self.wallet_widget_expenses = ttk.OptionMenu(controls, self.wallet_select_expenses, self.wallet_options[0], *self.wallet_options, command=lambda _ : self.update_periodicals())
        self.wallet_widget_expenses.pack(side=tk.LEFT, ipadx=8)

        self.root.wallet_update.append(self.update_expenses_wallets(controls))

        # Add expense periodical drop down
        ttk.Button(controls, text="Add Expense", style="Accent.TButton", command=self.AddPeriodicalExpense.run).pack(side=tk.RIGHT, padx=25)

        self.ViewPeriodicalExpense = ViewPeriodicalExpense(self.root)

        self.expenses = ttk.Treeview(expenses, columns=("note", "wallet", "frequency", "amount"))
        self.expenses.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.expenses.heading("#0", text="Next")
        self.expenses.column("#0", width=40)

        self.expenses.heading("note", text="Note")
        
        self.expenses.heading("wallet", text="Wallet")
        self.expenses.column("wallet", width=40, anchor=tk.CENTER)

        self.expenses.heading("frequency", text="Frequency")
        self.expenses.column("frequency", width=40, anchor=tk.CENTER)

        self.expenses.heading("amount", text="Amount")
        self.expenses.column("amount", width=40, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(expenses, orient=tk.VERTICAL, command=self.income.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.expenses.configure(yscrollcommand=scrollbar.set)
        self.expenses.bind("<Double-1>", self.expense_selected)
        
        self.root.periodicals_update.insert(0, self.calculate_periodicals)
        self.root.periodicals_update.append(self.update_periodicals)
        
        self.update_periodicals()
    
    def update_income_wallets(self, controls):
        
        def update():

            self.wallet_widget_income.destroy()

            self.wallet_options = self.root.mysql.all_wallets()
            self.wallet_options = ["All"] + [value for row in self.wallet_options for value in row]

            self.wallet_select_income = tk.StringVar(value=self.wallet_options[0])

            self.wallet_widget_income = ttk.OptionMenu(controls, self.wallet_select_income, self.wallet_options[0], *self.wallet_options, command=lambda _ : self.update_periodicals())
            self.wallet_widget_income.pack(side=tk.LEFT, ipadx=8)
        
        return update

    def update_expenses_wallets(self, controls):

        def update():

            self.wallet_widget_expenses.destroy()

            self.wallet_options = self.root.mysql.all_wallets()
            self.wallet_options = ["All"] + [value for row in self.wallet_options for value in row]

            self.wallet_select_expenses = tk.StringVar(value=self.wallet_options[0])

            self.wallet_widget_expenses = ttk.OptionMenu(controls, self.wallet_select_expenses, self.wallet_options[0], *self.wallet_options, command=lambda _ : self.update_periodicals())
            self.wallet_widget_expenses.pack(side=tk.LEFT, ipadx=8)
        
        return update
    
    def refresh(self):

        self.root.event_periodicals_update()
        self.root.event_expenses_update()
        self.root.event_income_update()

    def income_selected(self, event):

        # Get iid of record and run dialog
        id = self.income.identify_row(event.y)
        self.ViewPeriodicalIncome.run(id)
    
    def expense_selected(self, event):

        # Get iid of record and run dialog
        id = self.expenses.identify_row(event.y)
        self.ViewPeriodicalExpense.run(id)
    
    def calculate_periodicals(self):

        current = datetime.datetime.now()

        frequencies = (relativedelta(days=1), relativedelta(weeks=1), relativedelta(months=1), relativedelta(years=1))

        # Calculating income periodicals

        records = self.root.mysql.income_periodicals(self.sort_options.index(self.sort_selected_income.get()), self.wallet_select_income.get())

        for record in records:
            
            frequency = frequencies[record[3]]
            next = record[4]

            while next <= record[5] and next <= current:
                self.root.mysql.add_income((next, record[1], self.root.mysql.get_wallet_id_by_name(record[2])[0], record[6], "Added periodical income."))
                next += frequency
            
            if next > record[5]:
                self.root.mysql.delete_periodical_by_id(record[0])
                return

            self.root.mysql.update_periodical_by_id(record[0], (record[1], self.root.mysql.get_wallet_id_by_name(record[2])[0], None, record[3], next, record[5], record[6], False))
        
        # Calculating expense periodicals

        records = self.root.mysql.expense_periodicals(self.sort_options.index(self.sort_selected_expenses.get()), self.wallet_select_expenses.get())

        for record in records:
            
            frequency = frequencies[record[4]]
            next = record[5]

            while next <= record[6] and next <= current:
                self.root.mysql.add_expense((next, record[1], self.root.mysql.get_wallet_id_by_name(record[2])[0], self.root.mysql.get_category_id_by_name(record[3])[0], record[7], "Added periodical expense."))
                next += frequency
            
            if next > record[6]:
                self.root.mysql.delete_periodical_by_id(record[0])
                return

            self.root.mysql.update_periodical_by_id(record[0], (record[1], self.root.mysql.get_wallet_id_by_name(record[2])[0], self.root.mysql.get_category_id_by_name(record[3])[0], record[4], next, record[6], record[7], True))
    
    def update_periodicals(self):

        frequencies = ("Daily", "Weekly", "Monthly", "Yearly")

        records = self.root.mysql.income_periodicals(self.sort_options.index(self.sort_selected_income.get()), self.wallet_select_income.get())

        self.income.delete(*self.income.get_children())

        for record in records:
            self.income.insert("", "end", iid=record[0], text=record[4].date(), values=(record[1], record[2], frequencies[record[3]], record[6]))
        
        records = self.root.mysql.expense_periodicals(self.sort_options.index(self.sort_selected_expenses.get()), self.wallet_select_expenses.get())

        self.expenses.delete(*self.expenses.get_children())

        for record in records:
            self.expenses.insert("", "end", iid=record[0], text=record[5].date(), values=(record[1], record[2], frequencies[record[4]], record[7]))