import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from Views.frames import MainPageFrame


class HomePage(MainPageFrame):
    def __init__(self, parent):
        super().__init__("Home", parent)

        # Main content frame
        self.main_frame = tk.Frame(parent, bg='lightgray')
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Balance label
        self.balance_label = tk.Label(self.main_frame, text="Balance: $1000", font=("Helvetica", 24), bg='white')
        self.balance_label.pack(pady=20)

        # Transactions list
        self.transactions_label = tk.Label(self.main_frame, text="Previous Transactions:", font=("Helvetica", 18), bg='white')
        self.transactions_label.pack(pady=10)

        self.transactions_list = tk.Listbox(self.main_frame, font=("Helvetica", 14))
        self.transactions_list.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Sample transactions
        transactions = ["- $50 Grocery", "+ $200 Salary", "- $30 Gas", "- $100 Rent"]
        for transaction in transactions:
            self.transactions_list.insert(tk.END, transaction)
