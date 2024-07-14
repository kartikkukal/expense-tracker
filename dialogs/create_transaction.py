from tkinter import ttk
import tkinter as tk

class create_transaction:
    def __init__(self, root):
        self.root = root

    def run(self):

        # Create dialog

        self.dialog = tk.Toplevel()
        self.dialog.title("Create transaction")

        self.dialog.geometry("640x240")
        self.dialog.resizable(False, False)

        root_frame = ttk.Frame(self.dialog, padding="0 20 10 0")
        root_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        root_frame.grid_columnconfigure(tuple(range(5)), weight=1)

        # Note field

        ttk.Label(root_frame, text="Note:").grid(row=0, column=0, pady=(0, 10))

        note_entry = ttk.Entry(root_frame)
        note_entry.grid(row=0, column=1, columnspan=4, sticky="EW", pady=(0, 10))

        # Date/Time field

        ttk.Label(root_frame, text="Date/Time:").grid(row=1, column=0, pady=(0, 10))

        date_time_entry = ttk.Entry(root_frame, width=8)
        date_time_entry.grid(row=1, column=1, sticky="EW", pady=(0, 10))

        # Amount field

        ttk.Label(root_frame, text="Amount:").grid(row=1, column=2, pady=(0, 10))

        amount_entry = ttk.Entry(root_frame, width=6)
        amount_entry.grid(row=1, column=3, columnspan=2, sticky="EW", pady=(0, 10))

        # Category field

        self.sort_by_select = tk.StringVar(value="")

        ttk.Label(root_frame, text="Category:").grid(row=2, column=0, pady=(0, 10))
        
        ttk.OptionMenu(root_frame, self.sort_by_select, None, *self.root.cats).grid(row=2, column=1, columnspan=4, sticky="EW", pady=(0, 10))
    
        # Additional notes field

        ttk.Label(root_frame, text="Additional:").grid(row=3, column=0)        

        additional_entry = ttk.Entry(root_frame)
        additional_entry.grid(row=3, column=1, columnspan=4, sticky="EW")

        # Buttons frame

        button_frame = ttk.Frame(root_frame, padding="0 30 0 0")
        button_frame.grid(row=4, column=0, columnspan=5, sticky="EW",)

        ttk.Button(button_frame, text="Cancel", width=10, command=self.cancel_dialog).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Create", width=10, style="Accent.TButton").pack(side=tk.RIGHT, padx=(0, 10))

        # Show dialog

        self.dialog.transient(master=self.root.notebook)
        self.dialog.grab_set()
        self.root.notebook.wait_window(self.dialog)

    def create_transaction():
        pass

    def cancel_dialog(self):
        self.dialog.destroy()