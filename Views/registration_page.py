import tkinter as tk
from tkinter import ttk, Toplevel

from Controllers.RegistrationController import RegistrationController
from Controllers.WindowController import WindowController


class SignUpView:
    def __init__(self, root, window_controller, registration_controller):
        # Create a separate Toplevel window for the signup page
        self.root = Toplevel(root)
        self.root.title("Sign Up")

        # Store references to the controllers
        self.window_controller = window_controller
        self.registration_controller = registration_controller

        # Email Entry
        self.email_label = ttk.Label(self.root, text="Email")
        self.email_label.grid(row=0, column=0)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.grid(row=0, column=1)

        # Password Entry
        self.password_label = ttk.Label(self.root, text="Password")
        self.password_label.grid(row=1, column=0)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)

        # Secret Code Entry
        self.secret_code_label = ttk.Label(self.root, text="Secret Code")
        self.secret_code_label.grid(row=2, column=0)
        self.secret_code_entry = ttk.Entry(self.root)
        self.secret_code_entry.grid(row=2, column=1)

        # Confirm Button
        self.confirm_button = ttk.Button(self.root, text="Create Account", command=self.create_account)
        self.confirm_button.grid(row=3, column=1)

    def create_account(self):
        # Gather data and send it to the RegistrationController for registration
        email = self.email_entry.get()
        password = self.password_entry.get()
        secret_code = self.secret_code_entry.get()

        # Check if the registration controller is set and call the registration function
        if self.registration_controller:
            self.registration_controller.register_user(email, password, secret_code)

        # Close the Sign Up window upon successful registration
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()


    registration_controller = RegistrationController()

    reg = SignUpView(root, None, registration_controller)

    registration_controller.add_view(reg)

    root.mainloop()

