import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from Views.registration_page import SignUpView
from Controllers.RegistrationController import RegistrationController


class LoginView:
    def __init__(self, root):
        self.root = root
        self.controller = None
        self.root.title("MyBank")

        self.root.geometry('400x600')
        self.root.resizable(False, False)  # Make the window non-resizable

        # Bring the window to the front
        self.root.focus_force()

        # Center the window
        window_width = 400
        window_height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

        # Top frame for the image
        self.top_frame = tk.Frame(self.root, width=400, height=200)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH)

        # Centering the image vertically
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(2, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)

        # Load and display the image
        self.image = Image.open("assets/mybank-high-resolution-logo-transparent.png")
        self.image = self.image.resize((390, int(390 * 520 / 2000)), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self.top_frame, image=self.image)
        self.image_label.grid(row=1, column=0, pady=(20,0), padx = (15, 0))

        # Bottom frame for the login form
        self.bottom_frame = tk.Frame(self.root, width=400, height=300)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=0)

        # Centering the login form vertically
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(7, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        # Title Label
        self.title_label = ttk.Label(self.bottom_frame, text="👋 Login to your MyBank account",
                                     font=("Helvetica", 18, "bold"))
        self.title_label.grid(row=1, column=0, columnspan=2, pady= (0,20))

        # Email Label
        self.email_label = ttk.Label(self.bottom_frame, text="📧 Email", font= ("Helvetica", 14))
        self.email_label.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="w")

        # Custom style for rounded corners
        style = ttk.Style()
        style.configure("Rounded.TEntry", relief="flat", borderwidth=1, padding=5)
        style.map("Rounded.TEntry",
                  fieldbackground=[('active', 'white'), ('!active', 'white')],
                  background=[('active', 'white'), ('!active', 'white')],
                  bordercolor=[('active', 'gray'), ('!active', 'gray')])

        # Email Entry
        self.email_entry = ttk.Entry(self.bottom_frame, width=30, style="Rounded.TEntry")
        self.email_entry.grid(row=3, column=0, columnspan=2, pady=(0,15), padx=20, sticky="ew")


        # Password Label
        self.password_label = ttk.Label(self.bottom_frame, text="*️⃣ Password", font=("Helvetica", 14))
        self.password_label.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="w")

        # Password Entry
        self.password_entry = ttk.Entry(self.bottom_frame, width=30, show="*", style="Rounded.TEntry")
        self.password_entry.grid(row=5, column=0, columnspan=2, pady=(0, 15), padx=20, sticky="ew")

        # Secret Code Label
        self.secret_code_label = ttk.Label(self.bottom_frame, text="🤫 Secret Code", font=("Helvetica", 14))
        self.secret_code_label.grid(row=6, column=0, columnspan=2, pady=10, padx=20, sticky="w")

        # Secret Code Entry
        self.secret_code_entry = ttk.Entry(self.bottom_frame, width=30, show="*", style="Rounded.TEntry")
        self.secret_code_entry.grid(row=7, column=0, columnspan=2, pady=(0, 15), padx=20, sticky="ew")

        # Error message label (initially hidden)
        self.error_label = tk.Label(self.bottom_frame, text="", font=("Helvetica", 10), fg="red")
        self.error_label.grid(row=8, column=0, columnspan=2, pady=(0, 10))

        # Login Button
        self.login_button = ttk.Button(self.bottom_frame, text="Log in", width=10, command=self.login)
        self.login_button.grid(row=9, column=0, columnspan=2, pady=20, padx=20)

        # Sign-up link
        self.signup_label = tk.Label(self.bottom_frame,
                                     text="If you don't have an account, you can open a new one here!",
                                     font=("Helvetica", 10), fg="blue", cursor="hand2")
        self.signup_label.grid(row=10, column=0, columnspan=2, pady=(0, 20))
        # Update the signup_label binding in LoginView
        self.signup_label.bind("<Button-1>", lambda e: self.controller.open_signup(root))

    def login(self):
        if self.controller is not None:
            email = self.email_entry.get()
            password = self.password_entry.get()
            secret_code = self.secret_code_entry.get()
            self.controller.login(email, password, secret_code)

    # This function adds a controller to the view if it does not already have it
    def add_controller(self, controller):
        self.controller = controller

    def clean(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def show_error(self, message):
        self.clean()
        self.error_label.config(text=message)
        self.error_label.grid()
