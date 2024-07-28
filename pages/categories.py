from tkinter import ttk
import tkinter as tk

class categories:
    def __init__(self, root):

        # Initialize frames
        self.frame = ttk.Frame(root.notebook, padding="5")
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(tuple(range(2)), weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.categories = ttk.LabelFrame(self.frame, text="Top 5 categories")
        self.income = ttk.LabelFrame(self.frame, text="Income")
        self.spending = ttk.Frame(self.frame)
        
        padding_x = 5
        padding_y = 5
        
        self.categories.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="news")
        self.income.grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky="news")
        self.spending.grid(row=0, column=1, rowspan=2, padx=padding_x, pady=padding_y, sticky="news")

        self.controls = ttk.Frame(self.spending)
        self.controls.pack(side=tk.TOP)

        ttk.Label(self.controls, text="Sort by: ").pack(side=tk.LEFT, padx=20)

        self.sort_by_options = ("Newest first", "Oldest first")
        self.sort_by_select = tk.StringVar(value=self.sort_by_options[0])

        ttk.OptionMenu(self.controls, self.sort_by_select, self.sort_by_options[0], *self.sort_by_options).pack(side=tk.LEFT, padx=0, ipadx=15)

        self.list = ttk.LabelFrame(self.spending, text="Spending")
        self.list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

