import tkinter as tk
from tkinter import messagebox

from Controllers.WindowController import WindowController
from Models.user_model import UserModel
from Views.home_frame import HomePage
from Views.login_window import LoginView
from Views.main_window import MainWindow
from Views.send_money_frame import SendMoneyFrame
from Views.settings_frame import SettingsFrame


class LoginController:
    def __init__(self, view: LoginView):
        self.view = view
        view.add_controller(self)

    def login(self, username, password):
        # Verifica semplice delle credenziali
        try:
            if UserModel(username, password):
                self.view.root.destroy()  # Close the LoginView

                root = tk.Tk() # Create a new Tkinter root window

                window_controller = WindowController()
                main_window = MainWindow(root, window_controller)
                window_controller.add_window(main_window)
                  # Open the MainWindow
                root.mainloop()
        except ValueError:
            self.view.show_error("Invalid credentials")
        except Exception as e:
            self.view.show_error(str(e))


    def sign_up(self):
        messagebox.showinfo("Sign Up", "Sign Up feature not implemented yet")

