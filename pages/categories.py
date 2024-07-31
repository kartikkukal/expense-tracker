from tkinter import ttk
import tkinter as tk

class categories:
    def __init__(self, root):

        self.root = root

        # Initialize frames
        self.frame = ttk.Frame(root.notebook, padding="5")
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(tuple(range(2)), weight=1, uniform="fred")

        self.expenses_frame = ttk.Frame(self.frame)
        self.categories_frame = ttk.Frame(self.frame)
        
        padding_x = 5
        padding_y = 5

        self.expenses_frame.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="news")
        self.categories_frame.grid(row=0, column=1, padx=padding_x, pady=padding_y, sticky="news")

        self.controls = ttk.Frame(self.categories_frame)
        self.controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        ttk.Label(self.controls, text="Sort by: ").pack(side=tk.LEFT, padx=20)

        self.sort_by_options = ("Descending", "Ascending")
        self.sort_by_select = tk.StringVar(value=self.sort_by_options[0])

        ttk.OptionMenu(self.controls, self.sort_by_select, self.sort_by_options[0], *self.sort_by_options, command=self.select_sort_option).pack(side=tk.LEFT, ipadx=15)

        self.categories = ttk.Treeview(self.categories_frame, columns=("amount"))
        self.categories.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.categories.heading("#0", text="Category")
        self.categories.column("#0", width=1)
        self.categories.heading("amount", text="Amount")
        self.categories.column("amount", width=1)

        # Scrollbar with TreeView
        scrollbar = ttk.Scrollbar(self.categories_frame, orient=tk.VERTICAL, command=self.categories.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.categories.configure(yscrollcommand=scrollbar.set)
        self.categories.bind("<ButtonRelease-1>", self.get_expenses)

        self.expenses = ttk.Treeview(self.expenses_frame, columns=("amount"))
        self.expenses.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.expenses.heading("#0", text="Note")
        self.expenses.heading("amount", text="Amount")

        self.expenses.column("amount", width=1)

        self.root.expenses_update.append(self.update_categories)
        self.update_categories()
    
    def select_sort_option(self, *args):

        self.update_categories()
    
    def get_expenses(self, event):
        current = self.categories.focus()
        category = self.categories.item(current)["text"]

        ID = self.root.mysql.get_category_id(category)
        records = self.root.mysql.get_expense_by_category(ID[0])

        self.expenses.delete(*self.expenses.get_children())
        for record in records:
            self.expenses.insert("", "end", text=record[2], values=(record[4], ))

    def update_categories(self):

        self.categories.delete(*self.categories.get_children())

        sort = self.sort_by_options.index(self.sort_by_select.get())
        records = dict(self.root.mysql.category_spending(sort))

        categories = self.root.mysql.get_categories()

        for category in categories:
            if category[0] not in records:
                records[category[0]] = 0
        
        for category in records:
            amount = records[category]
            self.categories.insert("", "end", text=category, values=(amount))


