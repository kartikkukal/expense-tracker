from tkinter import ttk
import tkinter as tk

class Error:
    def __init__(self, root):

        self.root = root
    
    def show(self, message):

        self.message = message

        self.dialog = tk.Toplevel()
        self.dialog.minsize(width=120, height=60)
        self.dialog.title("Error")

        self.dialog.resizable(False, False)

        frame = ttk.Frame(self.dialog, padding="20 20 10 0")
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame.rowconfigure(tuple(range(2)), weight=1)
        frame.columnconfigure(tuple(range(2)), weight=1)
        
        ttk.Label(frame, text=self.message, wraplength=400, justify=tk.CENTER).grid(row=0, column=0, columnspan=2, pady=(0, 10), padx=20)

        button_frame = ttk.Frame(frame, padding="0 10 0 10")
        button_frame.grid(row=1, column=0, columnspan=2, sticky="EW")

        ttk.Button(button_frame, text="OK", command=self.dismiss).pack(side=tk.RIGHT, ipadx=15)

        self.dialog.transient(master=self.root.notebook)
        self.dialog.grab_set()
        self.root.notebook.wait_window(self.dialog)
    
    def dismiss(self):

        self.dialog.destroy()