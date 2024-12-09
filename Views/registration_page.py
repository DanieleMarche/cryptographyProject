import tkinter as tk
import os
from tkinter import ttk, Toplevel

# Uncomment these lines if the controllers are available
# from Controllers.RegistrationController import RegistrationController
# from Controllers.WindowController import WindowController
from tkinter import messagebox

import tkinter as tk
from tkinter import ttk

from Controllers import RegistrationController


class SignUpView:
    def __init__(self, root, controller: RegistrationController):
        self.root = root
        self.controller = controller
        self.root.title("MyBank SignUp")

        # Window Configuration
        self.root.geometry('400x600')
        self.root.resizable(False, False)
        self.root.focus_force()

        # Center the window on the screen
        window_width = 400
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

        # Bottom frame
        self.bottom_frame = tk.Frame(self.root, width=400, height=300)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=20)

        # Center the grid vertical
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(7, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        # Title
        self.title_label = ttk.Label(self.bottom_frame, text="Create your MyBank account",
                                     font=("Helvetica", 18, "bold"))
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Label and entry for User's name
        self.name_label = ttk.Label(self.bottom_frame, text="Name", font=("Helvetica", 14))
        self.name_label.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        self.name_entry = ttk.Entry(self.bottom_frame, width=30)
        self.name_entry.grid(row=3, column=0, columnspan=2, pady=(0, 15), padx=20, sticky="ew")

        # Label and entry for user's surname
        self.surname_label = ttk.Label(self.bottom_frame, text="Surname", font=("Helvetica", 14))
        self.surname_label.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        self.surname_entry = ttk.Entry(self.bottom_frame, width=30)
        self.surname_entry.grid(row=5, column=0, columnspan=2, pady=(0, 15), padx=20, sticky="ew")

        # Label and entry for user's email
        self.email_label = ttk.Label(self.bottom_frame, text="Email", font=("Helvetica", 14))
        self.email_label.grid(row=6, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        self.email_entry = ttk.Entry(self.bottom_frame, width=30)
        self.email_entry.grid(row=7, column=0, columnspan=2, pady=(0, 15), padx=20, sticky="ew")

        # Label and entry for password
        self.password_label = ttk.Label(self.bottom_frame, text="Password", font=("Helvetica", 14))
        self.password_label.grid(row=8, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        self.password_entry = ttk.Entry(self.bottom_frame, width=30, show="*")
        self.password_entry.grid(row=9, column=0, columnspan=2, pady=(0, 15), padx=20, sticky="ew")

        # Dropdow menu for CAs
        self.dropdown_label = ttk.Label(self.bottom_frame, text="Select a Certification Authority", font=("Helvetica", 14))
        self.dropdown_label.grid(row=10, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        self.dropdown_var = tk.StringVar()
        self.dropdown_menu = ttk.Combobox(self.bottom_frame, textvariable=self.dropdown_var, width=28, state="readonly")
        
        self.dropdown_menu['values'] = tuple(["Select an option"] + self.get_folders_in_path("Gerarquia_CAs/end_point_cas"))  # Opzioni fittizie
        self.dropdown_menu.grid(row=11, column=0, columnspan=2, pady=(0, 15), padx=20, sticky="ew")
        self.dropdown_menu.current(0)  # Seleziona la prima opzione di default
        

        # Registration button
        self.signup_button = ttk.Button(self.bottom_frame, text="Sign Up", width=10, command=self.signup)
        self.signup_button.grid(row=12, column=0, columnspan=2, pady=20, padx=20)

    def signup(self):
        # Ottieni i dati inseriti
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        ca = self.dropdown_var.get()

        self.controller

        self.controller.register(email, password, name, surname, ca)

    def show_message(self, message, color):
        self.root.destroy()
        messagebox.showinfo("Information", message)


    def show_error(self, message: str):
        self.clear_fields()  
        messagebox.showerror("Error", text=message)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)    
        self.email_entry.delete(0, tk.END)  
        self.password_entry.delete(0, tk.END)

    @staticmethod
    def get_folders_in_path(path):
        """
        Restituisce una tupla con i nomi di tutte le cartelle all'interno di uno specifico percorso.
        
        :param path: Percorso in cui cercare le cartelle.
        :return: Lista  con i nomi delle cartelle.
        """
        try:
            # Controlla che il percorso sia valido
            if not os.path.exists(path):
                raise ValueError(f"Path '{path}' not existing.")
            
            # Ottieni tutte le cartelle all'interno del percorso
            folders = [name for name in os.listdir(path)
                       if os.path.isdir(os.path.join(path, name))]
            
            return folders
        except Exception as e:
            print(f"Errore: {e}")
            return ()



if __name__ == "__main__":
    root = tk.Tk()

    # Uncomment these lines if the controllers are available
    # registration_controller = RegistrationController()
    # window_controller = WindowController()

    controller = RegistrationController()

    reg = SignUpView(root, controller)

    controller.add_view(reg)

    # Uncomment this line if the registration controller is available
    # registration_controller.add_view(reg)

    root.mainloop()
