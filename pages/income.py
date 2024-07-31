from tkinter import ttk
import tkinter as tk

class income:
    def __init__(self, root):

        # Initialize frames
        self.frame = ttk.Frame(root.notebook, padding=5)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(0, weight=3)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(tuple(range(2)), weight=1, uniform="fred")
        
        self.wallet_frame = ttk.Frame(self.frame)
        self.income = ttk.LabelFrame(self.frame, text="Income")
        
        self.list = ttk.Frame(self.frame)
        
        padding_x = 5
        padding_y = 5
        
        self.wallet_frame.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="news")
        self.income.grid(row=0, column=1, padx=padding_x, pady=padding_y, sticky="news")
        self.list.grid(row=1, column=0, columnspan=2, padx=padding_x, pady=padding_y, sticky="news")

        self.wallets = ttk.Treeview(self.wallet_frame, columns=("amount"))
        self.wallets.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.wallets.heading("#0", text="Wallet")
        self.wallets.column("#0", width=1)
        self.wallets.heading("amount", text="Amount")
        self.wallets.column("amount", width=1)

        scrollbar = ttk.Scrollbar(self.wallet_frame, orient=tk.VERTICAL, command=self.wallets.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.wallets.configure(yscrollcommand=scrollbar.set)


        self.income.grid_rowconfigure(tuple(range(2)), weight=1)
        self.income.grid_columnconfigure(0, weight=1)

        ttk.Label(self.income, text="Current balance: ", font=('Arial', 12)).grid(row=0, column=0, sticky="S")
        self.balance = ttk.Label(self.income, text="23,233$", font=('Arial', 32))
        self.balance.grid(row=1, column=0, sticky="N", pady=(8, 0))

        income_controls = ttk.Frame(self.list)
        income_controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        # Create sort by option menu
        ttk.Label(income_controls, text="Sort by: ").pack(side=tk.LEFT, padx=20)

        self.sort_by_options = ("Newest first", "Oldest first")
        self.sort_by_select = tk.StringVar(value=self.sort_by_options[0])

        ttk.OptionMenu(income_controls, self.sort_by_select, self.sort_by_options[0], *self.sort_by_options, command=self.select_sort_option).pack(side=tk.LEFT, padx=0, ipadx=15)

        # Add create transaction button
        ttk.Button(income_controls, text="Add Income", command=self.button_add_expense, style="Accent.TButton").pack(side=tk.RIGHT, padx=(0, 25))

        # Add create wallet button
        ttk.Button(income_controls, text="Create Wallet").pack(side=tk.RIGHT, padx=15)

        # Add TreeView
        self.income = ttk.Treeview(self.list, columns=("note", "wallet", "amount"))
        self.income.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.income.heading("#0", text="Date/Time")
        self.income.column("#0", width=80)

        self.income.heading("note", text="Note")

        self.income.heading("wallet", text="Wallet")
        self.income.column("wallet", width=40)

        self.income.heading("amount", text="Amount")
        self.income.column("amount", width=40, anchor=tk.CENTER)

        # Scrollbar with TreeView
        scrollbar = ttk.Scrollbar(self.list, orient=tk.VERTICAL, command=self.income.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.income.configure(yscrollcommand=scrollbar.set)

    def button_add_expense(self):
        print("Create transaction button pressed.")

    def select_sort_option(self, *args):
        index = self.sort_by_options.index(self.sort_by_select.get())
        print(index, self.sort_by_options[index])
    
    def select_time_range(self, *args):
        index = self.time_range_options.index(self.time_range_select.get())
        print(index, self.time_range_options[index])
