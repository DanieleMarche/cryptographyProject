import tkinter as tk

import Models.user_model
from Controllers.LoginController import *
from Models.user_model import UserModel
from Views.log_in_page_view import LoginView

if __name__ == "__main__":
    root = tk.Tk()

    # Creates the view
    view = LoginView(root)

    # Creates controller with the view
    model = UserModel()

    controller = LoginController(view, model)


    # Esecuzione della finestra
    root.mainloop()

