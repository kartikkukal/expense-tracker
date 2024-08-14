from tkinter import ttk
import tkinter as tk

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Overview:
    def __init__(self, root):

        # Set graph parameters
        mpl.rcParams["text.color"] = "white"
        mpl.rcParams["font.size"] = "15"

        self.root = root

        # Initialize root frame
        self.frame = ttk.Frame(root.notebook, padding=5)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(tuple(range(2)), weight=1, uniform="fred")
        self.frame.columnconfigure(tuple(range(2)), weight=1, uniform="fred")
        
        # Initialize frames
        self.categories = ttk.LabelFrame(self.frame, text="Expenses by catergory")
        balance = ttk.Labelframe(self.frame, text="Current balance")
        self.wallets = ttk.LabelFrame(self.frame, text="Expenses by wallet")
        periodicals = ttk.LabelFrame(self.frame, text="Periodicals")
        
        self.categories.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        balance.grid(row=0, column=1, padx=5, pady=5, sticky="news")
        self.wallets.grid(row=1, column=0, padx=5, pady=5, sticky="news")
        periodicals.grid(row=1, column=1, padx=5, pady=5, sticky="news")

        # Configure categories grid
        self.categories.rowconfigure(0, weight=1)
        self.categories.columnconfigure(0, weight=1)

        # Generate categories chart
        self.categories_chart = None
        self.categories_chart_update()

        # Configure balance grid
        balance.grid_rowconfigure(tuple(range(2)), weight=1)
        balance.grid_columnconfigure(0, weight=1)

        # Add balance labels
        self.balance = tk.IntVar(balance)
        self.balance_update()

        # Create current balance label
        ttk.Label(balance, text="Current balance: ", font=('Arial', 12)).grid(row=0, column=0, sticky="S")
        ttk.Label(balance, textvariable=self.balance, font=('Arial', 32)).grid(row=1, column=0, sticky="N", pady=(8, 0))

        # Configure wallets grid
        self.wallets.rowconfigure(0, weight=1)
        self.wallets.columnconfigure(0, weight=1)

        # Generate categories chart
        self.wallets_chart = None
        self.wallets_chart_update()
        

        # Register update methods
        self.root.expenses_update.append(self.categories_chart_update)
        self.root.expenses_update.append(self.wallets_chart_update)

        self.root.expenses_update.append(self.balance_update)
        self.root.income_update.append(self.balance_update)

    def categories_chart_update(self):

        # Get data for chart
        data = self.root.mysql.total_expense_by_category()

        # Delete old chart
        if self.categories_chart is not None:
            self.categories_chart.destroy()

        # Add no expense label when data is blank
        if len(data) == 0:

            for child in self.categories.winfo_children():
                child.destroy()

            ttk.Label(self.categories, text="No expenses", font=("Arial", 16)).grid(row=0, column=0)
            return
        
        # Create new chart with data
        label, amount = zip(*data)

        figure = Figure(dpi=45, facecolor="#1c1c1c")        
        figure.add_subplot().pie(amount, radius=1.2, labels=label)

        categories_chart = FigureCanvasTkAgg(figure, self.categories).get_tk_widget()
        categories_chart.grid(row=0, column=0, pady=5)
    
    def balance_update(self):

        balance = 0
        
        # Get cumulative income and add to balance
        income = dict(self.root.mysql.total_income_by_wallet())

        for wallet in income:
            balance += income[wallet]
        
        # Get cumulative expenses and subtract from balance
        expenses = dict(self.root.mysql.total_expense_by_wallet())

        for wallet in expenses:
            balance -= expenses[wallet]

        # Set balance
        self.balance.set(balance)

    def wallets_chart_update(self):

        # Get data for chart
        data = self.root.mysql.total_expense_by_wallet()

        # Delete old chart
        if self.wallets_chart is not None:
            self.wallets_chart.destroy()

        # Add no expense label when data is blank
        if len(data) == 0:

            for child in self.wallets.winfo_children():
                child.destroy()

            ttk.Label(self.wallets, text="No expenses", font=("Arial", 16)).grid(row=0, column=0)
            return
        
        # Create new chart with data
        label, amount = zip(*data)

        figure = Figure(dpi=45, facecolor="#1c1c1c")        
        figure.add_subplot().pie(amount, radius=1.2, labels=label)

        categories_chart = FigureCanvasTkAgg(figure, self.wallets).get_tk_widget()
        categories_chart.grid(row=0, column=0, pady=5)