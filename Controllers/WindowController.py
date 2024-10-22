import tkinter as tk
from tkinter import Frame

from Views.main_window import MainWindow

class WindowController:
    def __init__(self):
        self.window = None

    def change_frame(self, frame_name):
        """Mostra il frame specificato e nasconde gli altri."""
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



