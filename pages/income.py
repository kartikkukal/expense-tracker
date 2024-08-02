from tkinter import ttk
import tkinter as tk

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from dialogs.add_income import AddIncome
from dialogs.create_wallet import create_wallet
from dialogs.view_wallet import view_wallet

class Income:

    def __init__(self, root):

        self.root = root

        # Initialize root frame
        self.frame = ttk.Frame(root.notebook, padding=5)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(tuple(range(2)), weight=1)
        self.frame.columnconfigure(tuple(range(2)), weight=1, uniform="fred")
        
        # Initialize frames
        wallets = ttk.Frame(self.frame)
        income = ttk.Frame(self.frame)
        self.statistics = ttk.LabelFrame(self.frame, text="Balance")
        
        wallets.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        self.statistics.grid(row=0, column=1, padx=5, pady=5, sticky="news")
        income.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="news")

        # Wallets treeview
        self.wallets = ttk.Treeview(wallets, columns=("balance"))
        self.wallets.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.wallets.heading("#0", text="Wallet")
        self.wallets.column("#0", width=1)
        self.wallets.heading("balance", text="Balance")
        self.wallets.column("balance", width=1)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(wallets, orient=tk.VERTICAL, command=self.wallets.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create view wallet dialog
        self.view_wallet = view_wallet(root)

        # Bind double click event and scrollbar
        self.wallets.configure(yscrollcommand=scrollbar.set)
        self.wallets.bind("<Double-1>", self.wallet_selected)

        # Configure grid for statistics frame
        self.statistics.grid_rowconfigure(0, weight=1)
        self.statistics.grid_columnconfigure(0, weight=1)

        self.chart = None

        # Controls for income view
        controls = ttk.Frame(income)
        controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        # Sort by drop down
        ttk.Label(controls, text="Sort by: ").pack(side=tk.LEFT, padx=20)

        self.sort_by_options = ("Newest first", "Oldest first")
        self.sort_by_select = tk.StringVar(value=self.sort_by_options[0])

        ttk.OptionMenu(controls, self.sort_by_select, self.sort_by_options[0], *self.sort_by_options, command=lambda _ : self.update_income()).pack(side=tk.LEFT, ipadx=8)

        # Create add income dialog
        self.add_income = AddIncome(root)

        # Add income button
        ttk.Button(controls, text="Add Income", style="Accent.TButton", command=self.add_income.run).pack(side=tk.RIGHT, padx=25)

        # Create create wallet dialog
        self.create_wallet = create_wallet(root)

        # Create wallet button
        ttk.Button(controls, text="Create Wallet", command=self.create_wallet.run).pack(side=tk.RIGHT)

        # Income treeview
        self.income = ttk.Treeview(income, columns=("note", "wallet", "amount"))
        self.income.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.income.heading("#0", text="Date/Time")
        self.income.column("#0", width=80)

        self.income.heading("note", text="Note")

        self.income.heading("wallet", text="Wallet")
        self.income.column("wallet", width=40)

        self.income.heading("amount", text="Amount")
        self.income.column("amount", width=40, anchor=tk.CENTER)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(income, orient=tk.VERTICAL, command=self.income.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Register scrollbar
        self.income.configure(yscrollcommand=scrollbar.set)

        # Register update methods
        self.root.expenses_update.append(self.update_wallets)
        self.root.wallet_update.append(self.update_wallets)
        self.root.income_update.append(self.update_wallets)

        self.root.expenses_update.append(self.update_statistics)
        self.root.wallet_update.append(self.update_statistics)
        self.root.income_update.append(self.update_statistics)

        self.root.income_update.append(self.update_income)
        
        self.update_wallets()
        self.update_income()
        self.update_statistics()
    
    def wallet_selected(self, _):

        # Get current focused item
        current = self.wallets.focus()
        wallet = self.wallets.item(current)["text"]

        # Run view wallet dialog
        self.view_wallet.run(wallet)
    
    def update_wallets(self):

        # Get balance in each wallet
        self.balance = dict(self.root.mysql.total_income_by_wallet())
        wallets = self.root.mysql.all_wallets()

        # Set balance of all wallets
        for wallet in wallets:
            if wallet[0] not in self.balance:
                self.balance[wallet[0]] = 0
        
        # Get spending per wallet
        spending = dict(self.root.mysql.total_expense_by_wallet())

        # Subtract spending from balance
        for wallet in spending:
            self.balance[wallet] -= spending[wallet]

        # Update wallets treeview
        self.wallets.delete(*self.wallets.get_children())

        # Generate data for graph

        for wallet in self.balance:
            self.wallets.insert("", "end", text=wallet, values=(self.balance[wallet]))
    
    def update_statistics(self):

        labels = tuple(self.balance.keys())
        amount = tuple(self.balance.values())

        # Get absolute value of wallets
        amount = tuple(map(lambda x : abs(x), amount))

        if self.chart is not None:
            self.chart.destroy()

        figure = Figure(dpi=45, facecolor="#1c1c1c", figsize=(9, 4.4))        
        figure.add_subplot().pie(amount, radius=1.2, labels=labels)

        self.chart = FigureCanvasTkAgg(figure, self.statistics).get_tk_widget()
        self.chart.grid(row=0, column=0)
    
    def update_income(self):

        # Get income records
        order = self.sort_by_options.index(self.sort_by_select.get())
        records = self.root.mysql.all_income(order)

        # Update income treeview
        self.income.delete(*self.income.get_children())

        for record in records:
            self.income.insert("", "end", iid=record[0], text=record[1], values=(record[2], record[3], record[4]))
