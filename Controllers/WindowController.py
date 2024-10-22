import tkinter as tk
from tkinter import Frame

from Models.user_model import UserModel
from Views.main_window import MainWindow

class WindowController:
    def __init__(self):
        self.window = None
        self.usr_model = None

    def change_frame(self, frame_name):
        # Nascondi tutti i frame
        if self.window:
            for frame in self.window.frames.values():
                frame.pack_forget()

            # Mostra il frame selezionato
            frame = self.window.frames[frame_name]
            frame.pack(fill=tk.BOTH, expand=True)

    def add_window(self, window: MainWindow):
        self.window = window

        for frame in self.window.frames.values():
            frame.add_controller(self)

        self.change_frame("Home")

    def add_usr_model(self, usr_model: UserModel):
        self.usr_model = usr_model
        for frame in self.window.frames.values():
            frame.get_data(usr_model)



