from tkinter import ttk
import tkinter as tk

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sv_ttk

class overview:
    def __init__(self, root):

        self.root = root

        # Initialize frames
        self.frame = ttk.Frame(root.notebook, padding=5)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(tuple(range(2)), weight=1, uniform="fred")
        self.frame.columnconfigure(tuple(range(2)), weight=1, uniform="fred")
        
        # Initialize label frames
        self.categories = ttk.LabelFrame(self.frame, text="Catergories")
        self.income = ttk.Labelframe(self.frame, text="Income")
        self.expenses = ttk.LabelFrame(self.frame, text="expenses")
        self.periodicals = ttk.LabelFrame(self.frame, text="Periodicals")

        # Add label frames to the grid
        padding_x = 5
        padding_y = 5
        
        self.categories.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="news")
        self.income.grid(row=0, column=1, padx=padding_x, pady=padding_y, sticky="news")
        self.expenses.grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky="news")
        self.periodicals.grid(row=1, column=1, padx=padding_x, pady=padding_y, sticky="news")

        self.income.grid_rowconfigure(tuple(range(2)), weight=1)
        self.income.grid_columnconfigure(0, weight=1)

        ttk.Label(self.income, text="Current balance: ", font=('Arial', 12)).grid(row=0, column=0, sticky="S")
        self.balance = ttk.Label(self.income, text="23,233$", font=('Arial', 32))
        self.balance.grid(row=1, column=0, sticky="N", pady=(8, 0))


        mpl.rcParams["text.color"] = "white"
        mpl.rcParams["font.size"] = "15"

        self.root.expenses_update.append(self.categories_chart_update)

        self.categories_chart = None
        self.categories_chart_update()
        self.all_charts()

    def categories_chart_update(self):

        data = self.root.mysql.category_spending()

        if self.categories_chart is not None:
            self.categories_chart.destroy()

        if len(data) == 0:

            self.categories.rowconfigure(0, weight=1)
            self.categories.columnconfigure(0, weight=1)

            ttk.Label(self.categories, text="No expenses", font=("Arial", 16)).grid(row=0, column=0)

            return

        label, amount = zip(*data)

        figure = Figure(dpi=45, facecolor="#1c1c1c", figsize=(9, 4.8))        
        figure.add_subplot().pie(amount, radius=1.2, labels=label)

        self.categories_chart = FigureCanvasTkAgg(figure, self.categories).get_tk_widget()
        self.categories_chart.pack()
    
    def income_value_update():
        pass

    def all_charts(self):
        categories = ["Food & Beverages", "Rent", "Repairs", "Purchases", "EMIs"]
        values = [144, 352, 664, 332, 66]

        mpl.rcParams["text.color"] = "white"
        mpl.rcParams["font.size"] = "15"

        figure = Figure(dpi=45, facecolor="#1c1c1c", figsize=(9, 4.8))
        canvas = FigureCanvasTkAgg(figure, self.periodicals)
        canvas.get_tk_widget().config()
        axes = figure.add_subplot()

        axes.pie(values, radius=1.2, labels=categories)

        chart = FigureCanvasTkAgg(figure, self.periodicals)
        chart.get_tk_widget().pack()

        chart = FigureCanvasTkAgg(figure, self.expenses)
        chart.get_tk_widget().pack()