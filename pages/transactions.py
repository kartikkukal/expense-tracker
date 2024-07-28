from tkinter import ttk
import tkinter as tk

from dialogs.create_transaction import create_transaction
from dialogs.view_transaction import view_transaction

class transactions:
    def __init__(self, root):

        self.root = root

        # Initialize frames
        self.frame = ttk.Frame(root.notebook)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.controls = ttk.Frame(self.frame)
        self.controls.pack(side=tk.TOP, fill=tk.X)

        self.list = ttk.Frame(self.frame)
        self.list.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Create TreeView
        self.tree = ttk.Treeview(self.list, columns=("note", "category", "amount"))
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.heading("#0", text="Date/Time")
        self.tree.column("#0", width=80)

        self.tree.heading("note", text="Note")

        self.tree.heading("category", text="Category")
        self.tree.column("category", width=40)

        self.tree.heading("amount", text="Amount")
        self.tree.column("amount", width=40, anchor=tk.CENTER)

        # Scrollbar with TreeView
        scrollbar = ttk.Scrollbar(self.list, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.test)

        # Create sort by option menu
        ttk.Label(self.controls, text="Sort by: ").pack(side=tk.LEFT, padx=20, pady=10)

        self.sort_by_options = ("Newest first", "Oldest first")
        self.sort_by_select = tk.StringVar(value=self.sort_by_options[0])

        ttk.OptionMenu(self.controls, self.sort_by_select, self.sort_by_options[0], *self.sort_by_options, command=self.select_sort_option).pack(side=tk.LEFT, padx=0, pady=10, ipadx=15)

        # Create time range option menu
        ttk.Label(self.controls, text="Time range: ").pack(side=tk.LEFT, padx=20, pady=10)

        self.time_range_options = ("1 day", "7 days", "31 days", "90 days", "180 days", "1 Year")
        self.time_range_select = tk.StringVar(value=self.time_range_options[2])

        ttk.OptionMenu(self.controls, self.time_range_select, self.time_range_options[0], *self.time_range_options, command=self.select_time_range).pack(side=tk.LEFT, padx=0, pady=10, ipadx=15)

        self.create_transaction = create_transaction(root)
        self.view_transaction = view_transaction(root)

        # Add create transaction button
        ttk.Button(self.controls, text="Create transaction", command=self.create_transaction.run, style="Accent.TButton").pack(side=tk.RIGHT, padx=20, pady=10)

        self.root.updates.append(self.update_transactions)
        self.update_transactions()


    def select_sort_option(self, *args):

        self.update_transactions()
    
    def select_time_range(self, *args):

        self.update_transactions()
    
    def update_transactions(self):

        self.tree.delete(*self.tree.get_children())

        records = self.root.mysql.get_transactions(self.sort_by_options.index(self.sort_by_select.get()), self.time_range_options.index(self.time_range_select.get()))
        
        for record in records:
            self.tree.insert("", "end", iid=record[0], text=record[1], values=(record[2], record[3], record[4]))
    
    def test(self, event):
        iid = self.tree.identify_row(event.y)
        self.view_transaction.run(iid)
        