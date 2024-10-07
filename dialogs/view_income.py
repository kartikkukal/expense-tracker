from tkinter import ttk
import tkinter as tk

import datetime

class ViewIncome:

    def __init__(self, root):
        self.root = root

    def run(self, id):

        if id == "":
            return

        self.record = self.root.mysql.get_income_by_id(id)

        # Toplevel dialog frame
        self.dialog = tk.Toplevel()
        self.dialog.title("View Income")

        self.dialog.geometry("640x240")
        self.dialog.resizable(False, False)

        # Initialize root frame
        frame = ttk.Frame(self.dialog, padding="0 20 10 0")
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame.grid_columnconfigure(tuple(range(5)), weight=1)

        # Note entry
        ttk.Label(frame, text="Note:").grid(row=0, column=0, pady=(0, 10))

        self.note = tk.StringVar(frame, value=self.record[2])
        ttk.Entry(frame, textvariable=self.note).grid(row=0, column=1, columnspan=4, sticky="EW", pady=(0, 10))
    
        # Additional entry
        ttk.Label(frame, text="Additional:").grid(row=1, column=0, pady=(0, 10))        

        self.additional = tk.StringVar(frame, value=self.record[5])
        ttk.Entry(frame, textvariable=self.additional).grid(row=1, column=1, columnspan=4, sticky="EW", pady=(0, 10))

        # Wallet entry
        ttk.Label(frame, text="Wallet:").grid(row=2, column=0, pady=(0, 10))

        wallets = self.root.mysql.all_wallets()
        wallets = [value for row in wallets for value in row]
        self.wallet = tk.StringVar(value=self.root.mysql.get_wallet_by_id(self.record[3])[0])
        
        ttk.OptionMenu(frame, self.wallet, None,
                        *wallets).grid(row=2, column=1, sticky="EW", pady=(0, 10))
        
        # Amount entry
        ttk.Label(frame, text="Amount:").grid(row=2, column=2, padx=8, pady=(0, 10))

        self.amount = tk.StringVar(frame, value=self.record[4])
        ttk.Entry(frame, width=6, textvariable=self.amount).grid(row=2, column=3, columnspan=2, sticky="EW", pady=(0, 10))

        # Date entry
        ttk.Label(frame, text="Date:").grid(row=3, column=0)

        # Date frame
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=3, column=1, sticky="EW")

        current_date = self.record[1].date()
        
        # Year entry
        self.year = tk.StringVar(date_frame, value=current_date.year)
        ttk.Entry(date_frame, width=4, textvariable=self.year).grid(row=0, column=1, sticky="EW", padx=(0, 10))

        # Month entry
        self.month = tk.StringVar(date_frame, value=current_date.month)
        ttk.Entry(date_frame, width=2, textvariable=self.month).grid(row=0, column=2, sticky="EW", padx=(0, 10))

        # Day entry
        self.day = tk.StringVar(date_frame, value=current_date.day)
        ttk.Entry(date_frame, width=2, textvariable=self.day).grid(row=0, column=3, sticky="EW", padx=(0, 15))

        # Time frame
        time_frame = ttk.Frame(frame)
        time_frame.grid(row=3, column=2, sticky="EW")

        ttk.Label(time_frame, text="Time: ").grid(row=0, column=0, padx=(0, 10))

        current_time = self.record[1].time()

        # Hour entry
        self.hour = tk.StringVar(time_frame, value=current_time.hour)
        ttk.Entry(time_frame, width=2, textvariable=self.hour).grid(row=0, column=1, sticky="EW", padx=(0, 10))

        # Minute entry
        self.minute = tk.StringVar(time_frame, value=current_time.minute)
        ttk.Entry(time_frame, width=2, textvariable=self.minute).grid(row=0, column=2, sticky="EW")

        # Buttons frame
        button_frame = ttk.Frame(frame, padding="0 30 0 0")
        button_frame.grid(row=4, column=0, columnspan=5, sticky="EW",)

        ttk.Button(button_frame, text="Delete", width=10, command=self.delete_income).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Button(button_frame, text="Cancel", width=10, command=self.dialog.destroy).pack(side=tk.RIGHT)

        ttk.Button(button_frame, text="Update", width=10, 
                   style="Accent.TButton", command=self.update_income).pack(side=tk.RIGHT, padx=(0, 10))

        # Set dialog window as transient
        self.dialog.transient(master=self.root.notebook)

        # Wait for visibility and set grab
        self.dialog.wait_visibility()
        self.dialog.grab_set()

        # Wait for dialog to close
        self.root.notebook.wait_window(self.dialog)

    def delete_income(self):

        # Delete record and update treeview
        self.root.mysql.delete_income_by_id(self.record[0])
        self.root.event_income_update()

        # Close dialog
        self.dialog.destroy()

    def update_income(self):
        
        try:
            note = self.note.get()
            if note == "":
                raise ValueError("Note entry is empty")

            amount = self.amount.get()
            if not amount.isnumeric():
                raise ValueError("Amount entry is not numeric")
            
            wallet = self.root.mysql.get_wallet_id_by_name(self.wallet.get())[0]

            additional = self.additional.get()

            date_time = datetime.datetime(int(self.year.get()), int(self.month.get()), int(self.day.get()), int(self.hour.get()), int(self.minute.get()))

            # Update income record
            self.root.mysql.update_income_by_id(self.record[0], (date_time, note, wallet, amount, additional))
            self.root.event_income_update()

            self.dialog.destroy()
        
        except Exception as exception:
            self.root.error.show(exception)
            return