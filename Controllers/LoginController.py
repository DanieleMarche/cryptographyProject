from tkinter import messagebox

class LoginController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def login(self, username, password):
        # Verifica semplice delle credenziali
        if username == "admin" and password == "password":
            messagebox.showinfo("Login", "Login effettuato con successo!")
        else:
            messagebox.showerror("Errore", "Credenziali non valide")

