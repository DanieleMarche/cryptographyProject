import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import Image, ImageTk

from Views.frames import MainPageFrame


class MainWindow:
    def __init__(self, root, frames: dict[str:MainPageFrame]):
        self.root = root
        self.controller = None
        self.frames = frames
        self.root.title("MyBank Home Page")
        self.root.geometry('800x600')

        self.root.resizable(False, False)

        # Center the window
        window_width = 800
        window_height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

        # Sidebar frame
        self.sidebar_frame = tk.Frame(self.root, width=200, bg='white')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Main frame
        #self.main_frame = frames["Home"]
        #self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load and display the logo image
        self.logo_image = Image.open("assets/logo-myBank-mini.png")
        original_width, original_height = self.logo_image.size
        aspect_ratio = original_width / original_height
        new_width = 150
        new_height = int(new_width / aspect_ratio)
        self.logo_image = self.logo_image.resize((new_width, new_height), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.sidebar_frame, image=self.logo_photo, bg = 'white')
        self.logo_label.pack(pady=10)

        # Sidebar buttons
        self.home_button = customtkinter.CTkButton(self.sidebar_frame, text="Home", font=("Helvetica", 14),
                                            text_color="black",
                                            fg_color= "white",
                                            command=lambda: print("Send Money"),
                                            corner_radius=0,
                                            bg_color="white",
                                            hover_color= "white",
                                            border_width=0,
                                            state="disabled")
        self.home_button.pack(fill=tk.X, pady=10)

        # Separator
        self.separator3 = ttk.Separator(self.sidebar_frame, orient='horizontal')
        self.separator3.pack(fill=tk.X, pady=5, padx = 5)

        self.send_money_button = customtkinter.CTkButton(self.sidebar_frame, text="Send Money", font=("Helvetica", 14),
                                            text_color="black",
                                            fg_color= "white",
                                            command=lambda: print("Send Money"),
                                            corner_radius=0,
                                            bg_color="white",
                                            hover_color= "white",
                                            border_width=0,
                                            state="normal")
        self.send_money_button.pack(fill=tk.X, pady=10)

        # Separator
        self.separator3 = ttk.Separator(self.sidebar_frame, orient='horizontal')
        self.separator3.pack(fill=tk.X, pady=5, padx = 5)

        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="Settings", font=("Helvetica", 14),
                                            text_color="black",
                                            fg_color= "white",
                                            command=lambda: print("Settings"),
                                            corner_radius=0,
                                            bg_color="white",
                                            hover_color= "white",
                                            border_width=0,
                                            state="normal")
        self.settings_button.pack(fill=tk.X, pady=10)

    def change_frame(self, name):
        pass

    def add_controller(self, controller):
        self.controller = controller
