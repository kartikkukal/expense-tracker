from tkinter import ttk
import tkinter as tk

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sv_ttk

class overview:
    def __init__(self, root):

        # Initialize frames
        self.frame = ttk.Frame(root.notebook, padding=5)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(tuple(range(2)), weight=1)
        self.frame.columnconfigure(tuple(range(2)), weight=1)
        
        # Initialize label frames
        self.categories = ttk.LabelFrame(self.frame, text="Catergories")
        self.income = ttk.Labelframe(self.frame, text="Income")
        self.transactions = ttk.LabelFrame(self.frame, text="Transactions")
        self.periodicals = ttk.LabelFrame(self.frame, text="Periodicals")

        # Add label frames to the grid
        padding_x = 5
        padding_y = 5
        
        self.categories.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="news")
        self.income.grid(row=0, column=1, padx=padding_x, pady=padding_y, sticky="news")
        self.transactions.grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky="news")
        self.periodicals.grid(row=1, column=1, padx=padding_x, pady=padding_y, sticky="news")

        self.categories_chart()


    def categories_chart(self):
        categories = ["Food & Beverages", "Rent", "Repairs", "Purchases", "EMIs"]
        values = [144, 352, 664, 332, 66]

        mpl.rcParams["text.color"] = "white"
        mpl.rcParams["font.size"] = "15"

        figure = Figure(dpi=45, facecolor="#1c1c1c", figsize=(9, 4.8))
        canvas = FigureCanvasTkAgg(figure, self.categories)
        canvas.get_tk_widget().config()
        axes = figure.add_subplot()

        axes.pie(values, radius=1.2, labels=categories)

        chart = FigureCanvasTkAgg(figure, self.categories)
        chart.get_tk_widget().pack()

        chart = FigureCanvasTkAgg(figure, self.income)
        chart.get_tk_widget().pack()

        chart = FigureCanvasTkAgg(figure, self.periodicals)
        chart.get_tk_widget().pack()

        chart = FigureCanvasTkAgg(figure, self.transactions)
        chart.get_tk_widget().pack()