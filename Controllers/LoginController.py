import tkinter as tk
from tkinter import messagebox

import json

from Controllers.WindowController import WindowController
from Models.user_model import UserModel
from Views.login_window import LoginView
from Views.main_window import MainWindow
from Controllers.RegistrationController import RegistrationController
from Views.registration_page import RegistrationView


class LoginController:
    def __init__(self, view: LoginView):
        self.view = view
        view.add_controller(self)

        self.check_remembered_user()

    def check_remembered_user(self):
        try:
            with open('Documents/remember_user.json', 'r') as file:
                data = json.load(file)
                if data.get('email', '') != '':
                    self.view.email_entry.insert(0, data['email'])
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("Error decoding JSON")

    def login(self, username, password, secret_code):
        # Verifica semplice delle credenziali
        try:

            usr = UserModel(username, password, secret_code)

            self.view.root.destroy()  # Close the LoginView

            root = tk.Tk() # Create a new Tkinter root window

            window_controller = WindowController()
            main_window = MainWindow(root, window_controller)
            window_controller.add_window(main_window)
            window_controller.add_usr_model(usr)


            # Open the MainWindow
            root.mainloop()
        except ValueError:
            self.view.show_error("Invalid credentials")
        except Exception as e:
            self.view.show_error(str(e))


    def sign_up(self):
        registration_window = tk.Toplevel(self.view.root)
        registration_view = RegistrationView(registration_window)
        RegistrationController(registration_view)

