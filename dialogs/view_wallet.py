from tkinter import ttk
import tkinter as tk

class view_wallet:
    def __init__(self, root):    
        self.root = root
    
    def run(self, name):

        self.dialog = tk.Toplevel()
        self.dialog.title("View wallet")

        self.dialog.geometry("420x120")
        self.dialog.resizable(False, False)

        frame = ttk.Frame(self.dialog, padding="0 20 10 0")
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame.rowconfigure(tuple(range(2)), weight=1)
        frame.columnconfigure(tuple(range(2)), weight=1)
        
        ttk.Label(frame, text="Name: ").grid(row=0, column=0, pady=(0, 10))

        self.name_entry = tk.StringVar(frame, value=name)
        ttk.Entry(frame, textvariable=self.name_entry).grid(row=0, column=1, sticky="EW", pady=(0, 10))

        button_frame = ttk.Frame(frame, padding="0 10 0 10")
        button_frame.grid(row=1, column=0, columnspan=2, sticky="EW")

        ttk.Button(button_frame, text="Delete", width=10).pack(side=tk.LEFT, padx=(12, 0))
        ttk.Button(button_frame, text="Cancel", command=self.cancel_dialog, width=10).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Update", style="Accent.TButton", width=10).pack(side=tk.RIGHT)

        self.dialog.transient(master=self.root.notebook)
        self.dialog.grab_set()
        self.root.notebook.wait_window(self.dialog)

    def cancel_dialog(self):
        self.dialog.destroy()