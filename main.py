import tkinter as tk

from Controllers.LoginController import LoginController
from Views.login_window import LoginView

if __name__ == "__main__":
    root = tk.Tk()

    #Create the view
    view = LoginView(root)

    #Create the controller
    login_controller = LoginController(view)

    # Run the main loop
    root.mainloop()

