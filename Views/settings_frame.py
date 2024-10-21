import tkinter as tk
from tkinter import ttk

from Views.frames import MainPageFrame


class SettingsFrame(MainPageFrame):
    def __init__(self, parent):
        super().__init__("Settings", parent)

        # Title Label
        self.title_label = ttk.Label(self, text="Settings", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        # Option 1 Label and Entry
        self.option1_label = ttk.Label(self, text="Option 1:", font=("Helvetica", 14))
        self.option1_label.pack(pady=5)
        self.option1_entry = ttk.Entry(self, width=30)
        self.option1_entry.pack(pady=5)

        # Option 2 Label and Entry
        self.option2_label = ttk.Label(self, text="Option 2:", font=("Helvetica", 14))
        self.option2_label.pack(pady=5)
        self.option2_entry = ttk.Entry(self, width=30)
        self.option2_entry.pack(pady=5)

        # Save Button
        self.save_button = ttk.Button(self, text="Save", command=self.save_settings)
        self.save_button.pack(pady=20)

    def save_settings(self):
        option1 = self.option1_entry.get()
        option2 = self.option2_entry.get()
        # Add logic to save settings
        print(f"Settings saved: Option 1 = {option1}, Option 2 = {option2}")