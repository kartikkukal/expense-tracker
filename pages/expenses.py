from tkinter import ttk
import tkinter as tk

from dialogs.add_expense import AddExpense
from dialogs.view_expense import ViewExpense

class Expenses:
    
    def __init__(self, root):

        self.root = root

        # Initialize root frame
        self.frame = ttk.Frame(root.notebook, padding="10")
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Controls frame
        controls = ttk.Frame(self.frame)
        controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        # Sort by drop down
        ttk.Label(controls, text="Sort by: ").pack(side=tk.LEFT, padx=20)

        self.sort_options = ("Newest", "Oldest")
        self.sort_selected = tk.StringVar(value=self.sort_options[0])

        ttk.OptionMenu(controls, self.sort_selected, self.sort_options[0],
                        *self.sort_options, command=lambda _ : self.update_expenses()).pack(side=tk.LEFT, ipadx=8)

        # Time range drop down
        ttk.Label(controls, text="Time range: ").pack(side=tk.LEFT, padx=20)

        self.time_range_options = ("1 Day", "7 Days", "1 Month", "3 Months", "6 Months", "1 Year")
        self.time_range_select = tk.StringVar(value=self.time_range_options[2])

        ttk.OptionMenu(controls, self.time_range_select, self.time_range_options[2],
                        *self.time_range_options, command=lambda _ : self.update_expenses()).pack(side=tk.LEFT, ipadx=8)

        # Wallet drop down
        ttk.Label(controls, text="Wallet: ").pack(side=tk.LEFT, padx=20)

        self.wallet_options = self.root.mysql.all_wallets()
        self.wallet_options = ["All"] + [value for row in self.wallet_options for value in row]
        self.wallet_select = tk.StringVar(value=self.wallet_options[0])

        self.wallet_widget = ttk.OptionMenu(controls, self.wallet_select, self.wallet_options[0],
                        *self.wallet_options, command=lambda _ : self.update_expenses())
        self.wallet_widget.pack(side=tk.LEFT, ipadx=8)

        # Expenses treeview
        self.expenses = ttk.Treeview(self.frame, columns=("note", "category", "amount"))
        self.expenses.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.expenses.heading("#0", text="Date/Time")
        self.expenses.column("#0", width=80)

        self.expenses.heading("note", text="Note")

        self.expenses.heading("category", text="Category")
        self.expenses.column("category", width=40)

        self.expenses.heading("amount", text="Amount")
        self.expenses.column("amount", width=40, anchor=tk.CENTER)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.expenses.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create view expense dialog
        self.ViewExpense = ViewExpense(root)        

        # Bind double click event and scrollbar
        self.expenses.configure(yscrollcommand=scrollbar.set)
        self.expenses.bind("<Double-1>", self.expense_selected)

        # Create add expense dialog
        self.AddExpense = AddExpense(root)

        # Add create transaction button
        ttk.Button(controls, text="Add Expense", command=self.AddExpense.run, style="Accent.TButton").pack(side=tk.RIGHT, padx=25)

        # Register update method
        self.root.expenses_update.append(self.update_expenses)
        self.root.wallet_update.append(self.update_wallet(controls))

        # Run update methods
        self.update_expenses()
    
    def expense_selected(self, event):

        # Get iid of record and run dialog
        id = self.expenses.identify_row(event.y)
        self.ViewExpense.run(id)
    
    def update_wallet(self, controls):

        # Return update method
        def update():
            
            # Delete old OptionMenu
            self.wallet_widget.destroy()

            # Get wallet options list
            self.wallet_options = self.root.mysql.all_wallets()
            self.wallet_options = ["All"] + [value for row in self.wallet_options for value in row]
            self.wallet_select = tk.StringVar(value=self.wallet_options[0])

            # Create new OptionMenu
            self.wallet_widget = ttk.OptionMenu(controls, self.wallet_select, self.wallet_options[0], *self.wallet_options, command=lambda _ : self.update_expenses())
            self.wallet_widget.pack(side=tk.LEFT, ipadx=8)
        
        return update
    
    def update_expenses(self):

        # Get current expenses
        records = self.root.mysql.all_expenses(self.sort_options.index(self.sort_selected.get()), self.time_range_options.index(self.time_range_select.get()), self.wallet_select.get())
        
        # Update expenses treeview
        self.expenses.delete(*self.expenses.get_children())

        for record in records:
            self.expenses.insert("", "end", iid=record[0], text=record[1], values=(record[2], record[3], record[4]))