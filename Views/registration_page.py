from tkinter import ttk, messagebox
import tkinter as tk

class RegistrationView:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.controller = None

        # Username
        self.username_label = ttk.Label(root, text="Username")
        self.username_label.grid(row=0, column=0)
        self.username_entry = ttk.Entry(root)
        self.username_entry.grid(row=0, column=1)

        # Password
        self.password_label = ttk.Label(root, text="Password")
        self.password_label.grid(row=1, column=0)
        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1)

        # Secret Code
        self.secret_code_label = ttk.Label(root, text="Secret Code")
        self.secret_code_label.grid(row=2, column=0)
        self.secret_code_entry = ttk.Entry(root, show="*")
        self.secret_code_entry.grid(row=2, column=1)

        # Register Button
        self.register_button = ttk.Button(root, text="Register", command=self.register)
        self.register_button.grid(row=3, column=1)

    def register(self):
        if self.controller:
            username = self.username_entry.get()
            password = self.password_entry.get()
            secret_code = self.secret_code_entry.get()
            self.controller.register(username, password, secret_code)

    def add_controller(self, controller):
        self.controller = controller

    def show_message(self, message):
        messagebox.showinfo("Info", message)


