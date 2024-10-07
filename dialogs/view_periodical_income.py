from tkinter import ttk
import tkinter as tk

import datetime
import zoneinfo

from dialogs.confirmation import Confirmation

class ViewPeriodicalIncome:

    def __init__(self, root):
        self.root = root

    def run(self, id):

        if id == "":
            return

        self.record = self.root.mysql.get_periodical_by_id(id)

        # Toplevel dialog frame
        self.dialog = tk.Toplevel()
        self.dialog.title("Update Periodical")

        self.dialog.geometry("640x240")
        self.dialog.resizable(False, False)

        # Initialize root frame
        frame = ttk.Frame(self.dialog, padding="0 20 10 0")
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame.grid_columnconfigure(tuple(range(5)), weight=1)

        # Note entry
        ttk.Label(frame, text="Note:").grid(row=0, column=0, pady=(0, 10))

        self.note = tk.StringVar(frame, value=self.record[1])
        ttk.Entry(frame, textvariable=self.note).grid(row=0, column=1, columnspan=4, sticky="EW", pady=(0, 10))

        # Wallet entry
        ttk.Label(frame, text="Wallet:").grid(row=1, column=0, pady=(0, 10))

        wallets = self.root.mysql.all_wallets()
        wallets = [value for row in wallets for value in row]
        self.wallet = tk.StringVar(value=self.root.mysql.get_wallet_by_id(self.record[2])[0])
        
        ttk.OptionMenu(frame, self.wallet, None, *wallets).grid(row=1, column=1, sticky="EW", pady=(0, 10))

        # Frequency entry
        ttk.Label(frame, text="Frequency:").grid(row=1, column=2, pady=(0, 10))

        self.frequency_options = ("Daily", "Weekly", "Monthly", "Yearly")
        self.frequency_selected = tk.StringVar(value=self.frequency_options[self.record[4]])
        
        ttk.OptionMenu(frame, self.frequency_selected, None, *self.frequency_options).grid(row=1, column=3, columnspan=2, sticky="EW", pady=(0, 10))

        # Date entry
        ttk.Label(frame, text="Next:").grid(row=2, column=0, pady=(0, 10))

        # Date frame
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=2, column=1, sticky="EW", pady=(0, 10))

        till_date = self.record[5].date()
        
        # Year entry
        self.from_year = tk.StringVar(date_frame, value=till_date.year)
        ttk.Entry(date_frame, width=4, textvariable=self.from_year).grid(row=0, column=1, sticky="EW", padx=(0, 10))

        # Month entry
        self.from_month = tk.StringVar(date_frame, value=till_date.month)
        ttk.Entry(date_frame, width=2, textvariable=self.from_month).grid(row=0, column=2, sticky="EW", padx=(0, 10))

        # Day entry
        self.from_day = tk.StringVar(date_frame, value=till_date.day)
        ttk.Entry(date_frame, width=2, textvariable=self.from_day).grid(row=0, column=3, sticky="EW", padx=(0, 15))

        # Date entry
        ttk.Label(frame, text="Till:").grid(row=2, column=2, pady=(0, 10))

        # Date frame
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=2, column=3, sticky="EW", pady=(0, 10))

        till_date = self.record[6].date()
        
        # Year entry
        self.till_year = tk.StringVar(date_frame, value=till_date.year)
        ttk.Entry(date_frame, width=4, textvariable=self.till_year).grid(row=0, column=1, sticky="EW", padx=(0, 10))

        # Month entry
        self.till_month = tk.StringVar(date_frame, value=till_date.month)
        ttk.Entry(date_frame, width=2, textvariable=self.till_month).grid(row=0, column=2, sticky="EW", padx=(0, 10))

        # Day entry
        self.till_day = tk.StringVar(date_frame, value=till_date.day)
        ttk.Entry(date_frame, width=2, textvariable=self.till_day).grid(row=0, column=3, sticky="EW", padx=(0, 15))

        # Amount entry
        ttk.Label(frame, text="Amount:").grid(row=3, column=0)

        self.amount = tk.StringVar(frame, value=self.record[7])
        ttk.Entry(frame, width=6, textvariable=self.amount).grid(row=3, column=1, sticky="EW")

        # Buttons frame
        button_frame = ttk.Frame(frame, padding="0 30 0 0")
        button_frame.grid(row=5, column=0, columnspan=5, sticky="EW",)

        ttk.Button(button_frame, text="Delete", width=10, command=self.delete_periodical).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Button(button_frame, text="Cancel", width=10, command=self.dialog.destroy).pack(side=tk.RIGHT)

        ttk.Button(button_frame, text="Update", width=10, style="Accent.TButton", 
                   command=self.update_periodical).pack(side=tk.RIGHT, padx=(0, 10))

        # Show dialog
        self.dialog.transient(master=self.root.notebook)
        self.dialog.wait_visibility()
        self.dialog.grab_set()

        # Wait for dialog to close
        self.root.notebook.wait_window(self.dialog)
    
    def delete_periodical(self):

        # Delete record and update treeview
        self.root.mysql.delete_periodical_by_id(self.record[0])
        self.root.event_periodicals_update()

        # Close dialog
        self.dialog.destroy()

    def update_periodical(self):
        
        try:
            note = self.note.get()
            if note == "":
                raise ValueError("Note entry is empty")

            amount = self.amount.get()
            if not amount.isnumeric():
                raise ValueError("Amount entry is not numeric")
            
            wallet = self.root.mysql.get_wallet_id_by_name(self.wallet.get())[0]

            frequency = self.frequency_options.index(self.frequency_selected.get())

            from_date_time = datetime.datetime(int(self.from_year.get()), int(self.from_month.get()), int(self.from_day.get()), tzinfo=zoneinfo.ZoneInfo("Asia/Kolkata"))

            till_date_time = datetime.datetime(int(self.till_year.get()), int(self.till_month.get()), int(self.till_day.get()), tzinfo=zoneinfo.ZoneInfo("Asia/Kolkata"))

            if till_date_time <= from_date_time:
                raise ValueError("'till' date cannot be equal to 'from' date.")
            
            def update_periodical_execute():

                self.root.mysql.update_periodical_by_id(self.record[0], (note, wallet, None, frequency, from_date_time, till_date_time, amount, False))

                self.root.event_periodicals_update()
                self.root.event_income_update()
                self.dialog.destroy()
            
            if till_date_time < datetime.datetime.now(datetime.timezone.utc):
                self.root.debug_message("ViewPeriodicalIncome", "Till date time is less than current date.")
                Confirmation(self.root, "Since the till date is before current date, all the income entries will be added at once without creating an entry for perioidcal.", update_periodical_execute).show()
                return
            
            update_periodical_execute()
        
        except Exception as exception:
            self.root.error.show(exception)
            return