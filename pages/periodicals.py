from tkinter import ttk
import tkinter as tk

class periodicals:
    def __init__(self, root):

        # Initialize frame
        self.frame = ttk.Frame(root.notebook, padding="5")
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.controls = ttk.Frame(self.frame)
        self.controls.pack(side=tk.TOP, fill=tk.X, pady=(5, 0), padx=10)

        ttk.Button(self.controls, text="Add periodical").pack(side=tk.RIGHT)

        self.views = ttk.Frame(self.frame)
        self.views.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.views.rowconfigure(0, weight=1)
        self.views.columnconfigure(tuple(range(2)), weight=1, uniform="fred")

        self.income = ttk.Treeview(self.views, columns=("frequency", "till"))
        self.expense = ttk.Treeview(self.views, columns=("frequency", "till"))

        self.income.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        self.expense.grid(row=0, column=1, padx=5, pady=5, sticky="news")

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