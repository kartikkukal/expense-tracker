from tkinter import ttk
import tkinter as tk

class Confirmation:
    def __init__(self, root, message, callback):

        self.root = root
        self.message = message
        self.callback = callback
    
    def run(self):

        self.dialog = tk.Toplevel()
        self.dialog.title("Confirmation")

        self.dialog.resizable(False, False)

        frame = ttk.Frame(self.dialog, padding="0 20 10 0")
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame.rowconfigure(tuple(range(2)), weight=1)
        frame.columnconfigure(tuple(range(2)), weight=1)
        
        ttk.Label(frame, text=self.message, wraplength=400, justify=tk.CENTER).grid(row=0, column=0, columnspan=2, pady=(0, 10), padx=20)

        button_frame = ttk.Frame(frame, padding="0 10 0 10")
        button_frame.grid(row=1, column=0, columnspan=2, sticky="EW")

        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=(10, 0), ipadx=15)
        ttk.Button(button_frame, text="Confirm", style="Accent.TButton", command=self.execute).pack(side=tk.RIGHT, ipadx=15)

        self.dialog.transient(master=self.root.notebook)
        self.dialog.grab_set()
        self.root.notebook.wait_window(self.dialog)
    
    def execute(self):

        self.callback()
        self.dialog.destroy()