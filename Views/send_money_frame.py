import tkinter as tk
from tkinter import ttk

from Views.frames import MainPageFrame


class SendMoneyFrame(MainPageFrame):
    def __init__(self, parent):
        super().__init__("Send Money", parent)

        # Title Label
        self.title_label = ttk.Label(self, text="Send Money", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        # Recipient Label and Entry
        self.recipient_label = ttk.Label(self, text="User:", font=("Helvetica", 14))
        self.recipient_label.pack(pady=5)
        self.recipient_entry = ttk.Entry(self, width=30)
        self.recipient_entry.pack(pady=5)

        # Amount Label and Entry
        self.amount_label = ttk.Label(self, text="Amount:", font=("Helvetica", 14))
        self.amount_label.pack(pady=5)
        self.amount_entry = ttk.Entry(self, width=30)
        self.amount_entry.pack(pady=5)


        # Description Label and Entry
        self.description_label = ttk.Label(self, text="Description:", font=("Helvetica", 14))
        self.description_label.pack(pady=5)
        self.description_entry = tk.Entry(self, width=30)
        self.description_entry.pack(pady=5)

        # Send Button
        self.send_button = ttk.Button(self, text="Send", command=self.send_money)
        self.send_button.pack(pady=20)

    def send_money(self):
        recipient = self.recipient_entry.get()
        amount = self.amount_entry.get()
        description = self.description_entry.get()
        # Add logic to send money


if __name__ == "__main__":
    root = tk.Tk()
    frame = SendMoneyFrame(root)
    frame.pack(expand=True, fill=tk.BOTH)
    root.mainloop()