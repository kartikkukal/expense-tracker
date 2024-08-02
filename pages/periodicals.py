from tkinter import ttk
import tkinter as tk

class periodicals:
    def __init__(self, root):

        # Initialize frame
        self.frame = ttk.Frame(root.notebook, padding="5")
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        controls = ttk.Frame(self.frame)
        controls.pack(side=tk.TOP, fill=tk.X, pady=(5, 0), padx=10)

        ttk.Button(controls, text="Add periodical").pack(side=tk.RIGHT)

        views = ttk.Frame(self.frame)
        views.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        views.rowconfigure(0, weight=1)
        views.columnconfigure(tuple(range(2)), weight=1, uniform="fred")

        income = ttk.Frame(views)
        expense = ttk.Frame(views)
        
        income.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        expense.grid(row=0, column=1, padx=5, pady=5, sticky="news")

        self.income = ttk.Treeview(income, columns=("frequency", "till"))
        self.expense = ttk.Treeview(expense, columns=("frequency", "till"))

        self.income.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.expense.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.income.heading("#0", text="Title")
        self.income.heading("frequency", text="Frequency")
        self.income.heading("till", text="Till")

        self.income.column("#0", width=1)
        self.income.column("frequency", width=1)
        self.income.column("till", width=1)

        self.expense.heading("#0", text="Title")
        self.expense.heading("frequency", text="Frequency")
        self.expense.heading("till", text="Till")

        self.expense.column("#0", width=1)
        self.expense.column("frequency", width=1)
        self.expense.column("till", width=1)

        scrollbar = ttk.Scrollbar(income, orient=tk.VERTICAL, command=self.income.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar = ttk.Scrollbar(expense, orient=tk.VERTICAL, command=self.expense.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)