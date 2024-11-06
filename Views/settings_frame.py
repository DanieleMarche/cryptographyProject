import tkinter as tk
from tkinter import ttk

from Models.user_model import UserModel
from Views.frames import MainPageFrame


class SettingsFrame(MainPageFrame):
    def __init__(self, parent):
        super().__init__("Settings", parent)

        # Title Label
        self.title_label = ttk.Label(self, text="Settings", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        # Touch ID access Label and Toggle Switch
        self.touch_id_label = ttk.Label(self, text="Remember me and enable TouchID access:", font=("Helvetica", 14))
        self.touch_id_label.pack(pady=5)

        self.touch_id_var = tk.BooleanVar()
        self.touch_id_switch = ttk.Checkbutton(
            self,
            text="",
            style="Switch.TCheckbutton",
            variable=self.touch_id_var
        )
        self.touch_id_switch.pack(pady=5)

        # Save Button
        self.save_button = ttk.Button(self, text="Save", command=self.save_settings)
        self.save_button.pack(pady=20)

        # Define custom style for the switch
        style = ttk.Style()
        style.configure("Switch.TCheckbutton", font=("Helvetica", 14))
        style.map("Switch.TCheckbutton",
                  foreground=[('selected', 'green'), ('!selected', 'red')],
                  background=[('selected', 'lightgreen'), ('!selected', 'lightcoral')])

    def save_settings(self):
        self.controller.save_settings(self.touch_id_var.get())

    def set_data(self, model: UserModel):
        super().set_data(model)
        self.touch_id_var.set(model.touch_id)
