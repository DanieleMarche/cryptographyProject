import tkinter as tk
from tkinter import Frame, messagebox

from Cryptography.cryptography_utils import get_mac_address
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
            frame.set_data(usr_model)

    def save_settings(self, touch_id: bool):
        try:
            self.usr_model.touch_id = touch_id
            if touch_id:
                self.usr_model.touch_id_device = get_mac_address()
            else:
                self.usr_model.touch_id_device = None

            print(self.usr_model.touch_id)
            print(self.usr_model.touch_id_device)
            self.usr_model.save_user_data()
        except Exception as e:
            messagebox.showinfo(str(e))





