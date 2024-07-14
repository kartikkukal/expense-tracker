from pages.transactions import transactions
from pages.periodicals import periodicals
from pages.categories import categories
from pages.overview import overview
from pages.income import income

from tkinter import ttk
import tkinter as tk

import sv_ttk

global_thing = "test"

class root:
    def __init__(self):

        self.cats = []
        self.data = []


        # Intialize root window
        self.window = tk.Tk()
        self.window.title("Expense Tracker")
        self.window.geometry("860x540")
        self.window.resizable(False, False)

        # Intialize root frame
        self.frame = ttk.Frame(self.window)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Initialize root notebook
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Initialize overview
        self.overview = overview(self)
        self.notebook.add(self.overview.frame, text="Overview")

        # Initialize transactions
        self.transactions = transactions(self)
        self.notebook.add(self.transactions.frame, text="Transactions")

        # Initialize income
        self.income = income(self)
        self.notebook.add(self.income.frame, text="Income")

        # Initialize periodicals
        self.periodicals = periodicals(self)
        self.notebook.add(self.periodicals.frame, text="Periodicals")

        # Initialize categories
        self.categories = categories(self)
        self.notebook.add(self.categories.frame, text="Categories")

    def run(self):
        style = ttk.Style()
        sv_ttk._load_theme(style)
        style.theme_use("sun-valley-dark")
        self.window.mainloop()

def __main__():
    window = root()
    window.run()

if __name__ == "__main__":
    __main__()