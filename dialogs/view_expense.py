from tkinter import ttk
import tkinter as tk

import time

class view_expense:
    def __init__(self, root):
        self.root = root

    def run(self, id):

        self.record = self.root.mysql.get_expense(id)

        self.dialog = tk.Toplevel()
        self.dialog.title("View transaction")

        self.dialog.geometry("640x240")
        self.dialog.resizable(False, False)

        root_frame = ttk.Frame(self.dialog, padding="0 20 10 0")
        root_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        root_frame.grid_columnconfigure(tuple(range(5)), weight=1)

        # Note field

        ttk.Label(root_frame, text="Note:").grid(row=0, column=0, pady=(0, 10))

        self.note_entry = tk.StringVar(root_frame, value=self.record[2])
        ttk.Entry(root_frame, textvariable=self.note_entry).grid(row=0, column=1, columnspan=4, sticky="EW", pady=(0, 10))

        # Amount field

        ttk.Label(root_frame, text="Amount:").grid(row=1, column=0, pady=(0, 10))

        self.amount_entry = tk.StringVar(root_frame, value=str(self.record[4]))
        ttk.Entry(root_frame, width=6, textvariable=self.amount_entry).grid(row=1, column=1, sticky="EW", pady=(0, 10))

        # Category field

        ttk.Label(root_frame, text="Category:").grid(row=1, column=2, pady=(0, 10))

        self.categories = self.root.mysql.get_categories()

        self.category = tk.StringVar(value=self.categories[self.record[3] - 1][0])
        
        ttk.OptionMenu(root_frame, self.category, None, *self.categories).grid(row=1, column=3, columnspan=2, sticky="EW", pady=(0, 10))
    
        # Additional notes field

        ttk.Label(root_frame, text="Additional:").grid(row=2, column=0, pady=(0, 10))        

        self.additional_entry = tk.StringVar(root_frame, value=self.record[5])
        ttk.Entry(root_frame, textvariable=self.additional_entry).grid(row=2, column=1, columnspan=4, sticky="EW", pady=(0, 10))

        # Date/Time field

        ttk.Label(root_frame, text="Date:").grid(row=3, column=0)

        date_frame = ttk.Frame(root_frame)
        date_frame.grid(row=3, column=1, columnspan=4, sticky="EW")

        current_date = self.record[1]
        
        self.year_entry = tk.StringVar(date_frame, value=current_date.year)
        ttk.Entry(date_frame, width=5, textvariable=self.year_entry).grid(row=0, column=1, sticky="EW", padx=(0, 10))

        self.month_entry = tk.StringVar(date_frame, value=current_date.month)
        ttk.Entry(date_frame, width=3, textvariable=self.month_entry).grid(row=0, column=2, sticky="EW", padx=(0, 10))

        self.day_entry = tk.StringVar(date_frame, value=current_date.day)
        ttk.Entry(date_frame, width=3, textvariable=self.day_entry).grid(row=0, column=3, sticky="EW", padx=(0, 15))

        current_time = self.record[1]

        ttk.Label(date_frame, text="Time: ").grid(row=0, column=4, padx=(0, 10))

        self.hour_entry = tk.StringVar(date_frame, value=current_time.hour)
        ttk.Entry(date_frame, width=3, textvariable=self.hour_entry).grid(row=0, column=5, sticky="EW", padx=(0, 10))

        self.minute_entry = tk.StringVar(date_frame, value=current_time.minute)
        ttk.Entry(date_frame, width=3, textvariable=self.minute_entry).grid(row=0, column=6, sticky="EW")

        # Buttons frame

        button_frame = ttk.Frame(root_frame, padding="0 30 0 0")
        button_frame.grid(row=4, column=0, columnspan=5, sticky="EW",)

        ttk.Button(button_frame, text="Cancel", width=10, command=self.cancel_dialog).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Update", width=10, style="Accent.TButton", command=self.update_transcation).pack(side=tk.RIGHT, padx=(0, 10))

        # Show dialog

        self.dialog.transient(master=self.root.notebook)
        self.dialog.grab_set()
        self.root.notebook.wait_window(self.dialog)

    def update_transcation(self):

        year = self.year_entry.get()
        month = self.month_entry.get()
        day = self.day_entry.get()

        hour = self.hour_entry.get()
        minute = self.minute_entry.get()

        date_time = "/".join((year, month, day)) + " " + ":".join((hour, minute))

        category = self.categories.index((self.category.get(), )) + 1

        self.root.mysql.update_expense(self.record[0], (date_time, self.note_entry.get(), category, int(self.amount_entry.get()), self.additional_entry.get()))
        self.root.event_expenses_update()
        self.dialog.destroy()
    
    def cancel_dialog(self):
        self.dialog.destroy()