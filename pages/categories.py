from tkinter import ttk
import tkinter as tk

from dialogs.create_category import CreateCategory
from dialogs.view_category import ViewCategory

class Categories:
    
    def __init__(self, root):

        self.root = root

        # Initialize root frame
        self.frame = ttk.Frame(root.notebook, padding="5")
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(tuple(range(2)), weight=1, uniform="fred")

        # Initialize frames
        self.container = ttk.Frame(self.frame)
        categories = ttk.Frame(self.frame)

        self.container.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        categories.grid(row=0, column=1, padx=5, pady=5, sticky="news")

        # Category controls
        controls = ttk.Frame(categories)
        controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        # Sort by drop down
        ttk.Label(controls, text="Sort by: ").pack(side=tk.LEFT, padx=20)

        self.sort_options = ("Descending", "Ascending")
        self.sort_selected = tk.StringVar(value=self.sort_options[0])

        ttk.OptionMenu(controls, self.sort_selected, self.sort_options[0],
                        *self.sort_options, command=lambda _ : self.update_categories()).pack(side=tk.LEFT, ipadx=15)
        
        # Create create category dialog
        self.CreateCategory = CreateCategory(root)

        # Create new category button
        ttk.Button(controls, text="Create", style="Accent.TButton", command=self.CreateCategory.run).pack(side=tk.RIGHT, padx=(0, 25))

        # Categories treeview
        self.categories = ttk.Treeview(categories, columns=("amount"))
        self.categories.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=10)

        self.categories.heading("#0", text="Category")
        self.categories.column("#0", width=1)

        self.categories.heading("amount", text="Amount")
        self.categories.column("amount", width=1, anchor=tk.CENTER)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(categories, orient=tk.VERTICAL, command=self.categories.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.ViewCategory = ViewCategory(root)

        # Bind left click event and scrollbar
        self.categories.configure(yscrollcommand=scrollbar.set)
        self.categories.bind("<ButtonRelease-1>", self.category_clicked)
        self.categories.bind("<Double-1>", self.category_selected)

        self.treeview = False

        self.expenses = ttk.Label(self.container, text="Click on a category to see expenses.")
        self.expenses.pack(side=tk.TOP, expand=True)

        # Register update method
        self.root.expenses_update.append(self.update_categories)
        self.root.category_update.append(self.update_categories)
        self.update_categories() 
    
    def category_clicked(self, _):

        if not self.treeview:

            self.expenses.destroy()

            # Expenses treeview
            self.expenses = ttk.Treeview(self.container, columns=("amount"))
            self.expenses.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            self.expenses.heading("#0", text="Note")
            self.expenses.column("#0", width=1)

            self.expenses.heading("amount", text="Amount")
            self.expenses.column("amount", width=1, anchor=tk.CENTER)

            # Scrollbar for treeview
            scrollbar = ttk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.expenses.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Bind scrollbar
            self.expenses.configure(yscrollcommand=scrollbar.set)

            self.treeview = True

        # Get current focused item
        current = self.categories.focus()
        category = self.categories.item(current)["text"]

        # Get expenses by category
        records = self.root.mysql.get_expense_by_category(category)

        if len(records) == 0:
            
            self.expenses.destroy()

            for child in self.container.winfo_children():
                child.destroy()

            self.expenses = ttk.Label(self.container, text="No expenses in category.")
            self.expenses.pack(side=tk.TOP, expand=True)

            self.treeview = False

            return

        # Update expenses treeview
        self.expenses.delete(*self.expenses.get_children())
        
        for record in records:
            self.expenses.insert("", "end", text=record[2], values=(record[4], ))

    def category_selected(self, _):

        # Get current focused item
        current = self.categories.focus()
        category = self.categories.item(current)["text"]

        # Run view wallet dialog
        self.ViewCategory.run(category)

    def update_categories(self):

        # Get current spending by category
        sort = self.sort_options.index(self.sort_selected.get())
        records = dict(self.root.mysql.total_expense_by_category(sort))

        # Get all categories
        categories = self.root.mysql.all_categories()

        # Set all missing categories to 0
        for category in categories:
            if category[0] not in records:
                records[category[0]] = 0
        
        # Update expenses treeview
        self.categories.delete(*self.categories.get_children())

        for category in records:
            self.categories.insert("", "end", text=category, values=(records[category], ))


