from tkinter import ttk
import tkinter as tk

class ViewExpense:

    def __init__(self, root):
        self.root = root

    def run(self, id):

        # Toplevel dialog frame
        self.dialog = tk.Toplevel()
        self.dialog.title("View transaction")

        self.dialog.geometry("640x240")
        self.dialog.resizable(False, False)

        # Initialize root frame
        frame = ttk.Frame(self.dialog, padding="0 20 10 0")
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame.grid_columnconfigure(tuple(range(5)), weight=1)

        # Get details of record
        self.record = self.root.mysql.get_expense_by_id(id)

        # Note entry
        ttk.Label(frame, text="Note:").grid(row=0, column=0, pady=(0, 10))

        self.note = tk.StringVar(frame, value=self.record[2])
        ttk.Entry(frame, textvariable=self.note).grid(row=0, column=1, columnspan=4, sticky="EW", pady=(0, 10))

         # Wallet entry
        ttk.Label(frame, text="Wallet:").grid(row=1, column=0, pady=(0, 10))

        self.wallets = self.root.mysql.all_wallets()
        self.wallets = [value for row in self.wallets for value in row]
        self.wallet = tk.StringVar(value=self.wallets[self.record[3] - 1])
        
        ttk.OptionMenu(frame, self.wallet, self.wallets[0],
                        *self.wallets).grid(row=1, column=1, sticky="EW", pady=(0, 10))
        
        # Category entry
        ttk.Label(frame, text="Category:").grid(row=1, column=2, pady=(0, 10))

        self.categories = self.root.mysql.all_categories()
        self.categories = [value for row in self.categories for value in row]
        self.category = tk.StringVar(value=self.categories[self.record[4] - 1])
        
        ttk.OptionMenu(frame, self.category, None, *self.categories).grid(row=1, column=3, columnspan=2, sticky="EW", pady=(0, 10))
    
        # Additional entry
        ttk.Label(frame, text="Additional:").grid(row=2, column=0, pady=(0, 10))        

        self.additional = tk.StringVar(frame, value=self.record[6])
        ttk.Entry(frame, textvariable=self.additional).grid(row=2, column=1, columnspan=4, sticky="EW", pady=(0, 10))

        # Date entry
        ttk.Label(frame, text="Date:").grid(row=3, column=0)

        # Date frame
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=3, column=1, sticky="EW")

        current_date = self.record[1]
        
        # Year entry
        self.year = tk.StringVar(date_frame, value=current_date.year)
        ttk.Entry(date_frame, width=5, textvariable=self.year).grid(row=0, column=1, sticky="EW", padx=(0, 10))

        # Month entry
        self.month = tk.StringVar(date_frame, value=current_date.month)
        ttk.Entry(date_frame, width=3, textvariable=self.month).grid(row=0, column=2, sticky="EW", padx=(0, 10))

        # Day entry
        self.day = tk.StringVar(date_frame, value=current_date.day)
        ttk.Entry(date_frame, width=3, textvariable=self.day).grid(row=0, column=3, sticky="EW", padx=(0, 15))
        
        # Time frame
        time_frame = ttk.Frame(frame)
        time_frame.grid(row=3, column=2, sticky="EW")

        ttk.Label(time_frame, text="Time: ").grid(row=0, column=0, padx=(0, 10))

        current_time = self.record[1]
        
        # Hour entry
        self.hour = tk.StringVar(date_frame, value=current_time.hour)
        ttk.Entry(time_frame, width=3, textvariable=self.hour).grid(row=0, column=1, sticky="EW", padx=(0, 10))

        # Minute entry
        self.minute = tk.StringVar(date_frame, value=current_time.minute)
        ttk.Entry(time_frame, width=3, textvariable=self.minute).grid(row=0, column=2, sticky="EW")

        # Amount entry
        ttk.Label(frame, text="Amount:").grid(row=3, column=3)
        
        self.amount = tk.StringVar(frame, value=str(self.record[5]))
        ttk.Entry(frame, width=6, textvariable=self.amount).grid(row=3, column=4, sticky="EW")

        # Buttons frame
        button_frame = ttk.Frame(frame, padding="0 30 0 0")
        button_frame.grid(row=4, column=0, columnspan=5, sticky="EW",)

        ttk.Button(button_frame, text="Delete", width=10, command=self.delete_expense).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Button(button_frame, text="Cancel", width=10, command=self.dialog.destroy).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Update", width=10, style="Accent.TButton", command=self.update_transcation).pack(side=tk.RIGHT, padx=(0, 10))

        # Show dialog
        self.dialog.transient(master=self.root.notebook)
        self.dialog.grab_set()

        # Wait for dialog to close
        self.root.notebook.wait_window(self.dialog)
    
    def delete_expense(self):

        # Delete record and update treeview
        self.root.mysql.delete_expense_by_id(self.record[0])
        self.root.event_expenses_update()

        # Close dialog
        self.dialog.destroy()

    def update_transcation(self):

        try:
            note = self.note.get()
            if note == "":
                raise ValueError("Note entry is empty")

            amount = self.amount.get()
            
            wallet = self.wallets.index(self.wallet.get()) + 1
            category = self.categories.index(self.category.get()) + 1

            additional = self.additional.get()

            year = int(self.year.get())
            month = int(self.month.get())
            day = int(self.day.get())

            hour = int(self.hour.get())
            minute = int(self.minute.get())

            date_time = "{}/{}/{} {}:{}:00".format(year, month, day, hour, minute)

            # Update expense record
            self.root.mysql.update_expense_by_id(self.record[0], (date_time, note, wallet, category, amount, additional))
            self.root.event_expenses_update()

            self.dialog.destroy()

        except Exception as e:
            print(e)
            return