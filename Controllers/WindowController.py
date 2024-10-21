from tkinter import Frame

from Views.main_window import MainWindow


class WindowController:
    def __init__(self, window: MainWindow, frames: dict[str:Frame]):
        self.window = window
        window.add_controller(self)

        self.frames = frames
        for frame in frames.values():
            frame.add_controller(self)
        self.current_frame = list(frames.values())[0]

        window.change_frame(self.current_frame)

    def change_frame(self, frame_name):
        self.current_frame.pack_forget()
        self.current_frame = self.frames[frame_name]
        self.current_frame.pack()



