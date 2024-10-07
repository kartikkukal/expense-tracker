from tkinter import ttk
import tkinter as tk

from dialogs.confirmation import Confirmation

class ViewCategory:
    def __init__(self, root):    
        self.root = root
    
    def run(self, name):

        if name == "":
            return
        
        self.id = self.root.mysql.get_category_id_by_name(name)[0]

        self.dialog = tk.Toplevel()
        self.dialog.title("View category")

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

        self.Confirmation = Confirmation(self.root, "This operation will delete all records related to this category. Are you sure you want to delete this category?", self.delete_category)

        ttk.Button(button_frame, text="Delete", command=self.Confirmation.show, width=10).pack(side=tk.LEFT, padx=(12, 0))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy, width=10).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Update", style="Accent.TButton", command=self.update_category, width=10).pack(side=tk.RIGHT)

        # Set dialog window as transient
        self.dialog.transient(master=self.root.notebook)

        # Wait for visibility and set grab
        self.dialog.wait_visibility()
        self.dialog.grab_set()

        # Wait for dialog to close
        self.root.notebook.wait_window(self.dialog)

    def delete_category(self):
        
        self.root.mysql.delete_expense_by_category(self.id)
        self.root.mysql.delete_category_by_id(self.id)
        self.root.event_expenses_update()
        self.dialog.destroy()

    def update_category(self):
        
        name = self.name_entry.get()

        if name == "":
            self.root.error.show("Name entry is empty")
            return
        
        self.root.mysql.update_category_by_id(self.id, name)
        self.root.event_expenses_update()

        self.dialog.destroy()