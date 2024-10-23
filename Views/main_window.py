import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import Image, ImageTk

from Views.home_frame import HomePage
from Views.send_money_frame import SendMoneyFrame
from Views.settings_frame import SettingsFrame


class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

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

        # Main frame container
        self.main_frame = tk.Frame(self.root, bg='lightgray')
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Dizionario dei frame
        self.frames = {
            "Home": HomePage(self.main_frame),
            "Send Money": SendMoneyFrame(self.main_frame),
            "Settings": SettingsFrame(self.main_frame, )
        }

        # Load and display the logo image
        self.logo_image = Image.open("assets/logo-myBank-mini.png")
        original_width, original_height = self.logo_image.size
        aspect_ratio = original_width / original_height
        new_width = 150
        new_height = int(new_width / aspect_ratio)
        self.logo_image = self.logo_image.resize((new_width, new_height), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.sidebar_frame, image=self.logo_photo, bg='white')
        self.logo_label.pack(pady=10)

        # Generate buttons for each frame
        for frame_name in self.frames.keys():
            button = customtkinter.CTkButton(
                self.sidebar_frame,
                text=frame_name,
                font=("Helvetica", 14),
                text_color="black",
                fg_color="white",
                command=lambda name=frame_name: self.controller.change_frame(name),
                corner_radius=0,
                bg_color="white",
                hover_color="white",
                border_width=0,
                state="normal"
            )
            button.pack(fill=tk.X, pady=10)

