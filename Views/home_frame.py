import tkinter as tk

from Views.frames import MainPageFrame

class HomePage(MainPageFrame):
    def __init__(self, parent):
        super().__init__("Home", parent)
        self.name = ""
        self.balance = 0.00
        self.transactions = []

        # Greeting label
        self.greeting_label = tk.Label(self, text=f"Hi {self.name}!", font=("Helvetica", 24))
        self.greeting_label.pack(pady=20)

        # Balance label
        self.balance_label = tk.Label(self, text="Balance: " + str(self.balance), font=("Helvetica", 24))
        self.balance_label.pack(pady=20)

        # Transactions list
        self.transactions_label = tk.Label(self, text="Previous Transactions:", font=("Helvetica", 18))
        self.transactions_label.pack(pady=10)

        self.transactions_list = tk.Listbox(self, font=("Helvetica", 14))
        self.transactions_list.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Sample transactions
        for transaction in self.transactions:
            self.transactions_list.insert(tk.END, transaction)


    def set_data(self, model):
        self.name = model.name
        self.balance = model.balance
        self.transactions = model.transactions

        self.greeting_label.config(text=f"Hi {self.name}!")
        self.balance_label.config(text="Balance: " + str(self.balance) + "€")

        self.transactions_list.delete(0, tk.END)
        for transaction in self.transactions:
            if transaction["user1"] == model.username:
                self.transactions_list.insert(tk.END, f"{transaction["created_at"]} Sent {transaction['money']}€ to {transaction['user2']} with description: '{transaction['description']}'")
            else: 
                self.transactions_list.insert(tk.END, f"{transaction["created_at"]} Received {transaction['money']}€ from {transaction['user1']} with description: '{transaction['description']}'")