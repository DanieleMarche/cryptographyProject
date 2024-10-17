import tkinter as tk


class LoginView:
    def __init__(self, master):
        self.master = master
        self.master.title("Login - Home Banking")
        self.master.geometry("300x200")

        # Ottieni le dimensioni dello schermo
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        #Wisth and height
        window_width = 300
        window_height = 200

        # Calcola la posizione x e y per centrare la finestra
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Imposta la geometria della finestra
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Label e campo di input per il nome utente
        self.label_username = tk.Label(master, text="Nome utente")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(master)
        self.entry_username.pack(pady=5)

        # Label e campo di input per la password
        self.label_password = tk.Label(master, text="Password")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(master, show="*")  # show="*" per nascondere la password
        self.entry_password.pack(pady=5)

        # Pulsante di login
        self.btn_login = tk.Button(master, text="Login", command=self.login)
        self.btn_login.pack(pady=10)

        # Pulsante di uscita
        self.btn_exit = tk.Button(master, text="Esci", command=master.quit)
        self.btn_exit.pack(pady=5)


        # Porta la finestra in primo piano
        self.master.attributes("-topmost", True)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Chiama il controller per gestire il login
        print("login")


