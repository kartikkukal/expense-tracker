from pages.periodicals import periodicals
from pages.categories import Categories
from pages.overview import overview
from pages.expenses import Expenses
from pages.income import Income
from database import Database

from tkinter import ttk
import tkinter as tk

import sv_ttk

class root:
    def __init__(self):

        self.mysql = Database()

        # Intialize root window
        self.window = tk.Tk()
        self.window.title("Expense Tracker")
        self.window.geometry("860x540")

        # List of functions to run on update
        self.expenses_update = []
        self.income_update = []
        self.wallet_update = []

        # Intialize root frame
        self.frame = ttk.Frame(self.window)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Initialize root notebook
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Initialize overview
        self.overview = overview(self)
        self.notebook.add(self.overview.frame, text="Overview")

        # Initialize expenses
        self.expenses = Expenses(self)
        self.notebook.add(self.expenses.frame, text="Expenses")

        # Initialize income
        self.income = Income(self)
        self.notebook.add(self.income.frame, text="Income")

        # Initialize categories
        self.categories = Categories(self)
        self.notebook.add(self.categories.frame, text="Categories")

        # Initialize periodicals
        self.periodicals = periodicals(self)
        self.notebook.add(self.periodicals.frame, text="Periodicals")

    def run(self):
        sv_ttk.set_theme("dark")
        self.window.mainloop()
    
    def event_expenses_update(self):
        for function in self.expenses_update:
            function()
    
    def event_income_update(self):
        for function in self.income_update:
            function()
    
    def event_wallet_update(self):
        for function in self.wallet_update:
            function()

def __main__():
    window = root()
    window.run()

if __name__ == "__main__":
    __main__()