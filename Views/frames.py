import tkinter as tk

from Models.user_model import UserModel


class MainPageFrame(tk.Frame):
    _instances = {}  # Dizionario che contiene le istanze delle sottoclassi
    name = None
    surname = None

    balance = None

    def __new__(cls, *args, **kwargs):
        """Crea una nuova istanza solo se non esiste già per quella classe."""
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self, name: str, parent):
        super().__init__(parent)
        self.name = name
        self.controller = None

    def add_controller (self, controller):
        self.controller = controller

    def get_data(self, model: UserModel):
        self.name = model.name
        self.surname = model.surname
        self.balance = model.balance



