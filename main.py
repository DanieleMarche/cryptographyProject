import tkinter as tk

import Models.user_model
from Controllers.LoginController import *
from Models.user_model import UserModel
from Views.login_window import LoginView

if __name__ == "__main__":
    root = tk.Tk()

    # Creates the model
    model = UserModel()

    #Create the view
    view = LoginView(root)

    #Create the controller
    login_controller = LoginController(view, model)

    # Run the main loop
    root.mainloop()

