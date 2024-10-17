from tkinter import messagebox

class LoginController:
    def __init__(self, model):

        self.model = model

    def login(self, username, password):
        # Verifica semplice delle credenziali
        if username == "admin" and password == "password":
            messagebox.showinfo("Login", "Login effettuato con successo!")
        else:
            messagebox.showerror("Errore", "Credenziali non valide")

    def authenticate(self, email, password):
        if email == "user@example.com" and password == "password123":
            messagebox.showinfo("Login Success", "Login successful!")
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    def sign_up(self):
        messagebox.showinfo("Sign Up", "Redirecting to Sign Up Page...")

