import tkinter as tk
from tkinter import messagebox

from Controllers.WindowController import WindowController
from Views.home_frame import HomePage
from Views.login_window import LoginView
from Views.main_window import MainWindow
from Views.send_money_frame import SendMoneyFrame
from Views.settings_frame import SettingsFrame


class LoginController:
    def __init__(self, view: LoginView, model):
        self.view = view
        view.add_controller(self)
        self.model = model

    def login(self, username, password):
        # Verifica semplice delle credenziali
        if username == "admin" and password == "password":
            self.view.root.destroy()  # Close the LoginView
            root = tk.Tk() # Create a new Tkinter root window
            frames = {frames.name: frames for frames in [HomePage(root), SendMoneyFrame(root), SettingsFrame(root)]}
            main_window = MainWindow(root, frames)

            window_controller = WindowController(main_window, frames)  # Create a new WindowController
              # Open the MainWindow
            root.mainloop()
        else:
            messagebox.showerror("Errore", "Credenziali non valide")

