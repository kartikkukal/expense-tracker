from tkinter import ttk
import tkinter as tk

class categories:
    def __init__(self, root):

        # Initialize frames
        self.frame = ttk.Frame(root.notebook)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)