import tkinter as tk
import hmac
import hashlib


from tkinter import messagebox
from DataBase.database_utils import *
from Models.user_model import UserModel
from Views.main_window import MainWindow


def generate_auth_tag(message, key):
    mac = hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
    print(f"Generated MAC: {mac}, Algorithm: HMAC-SHA256, Key Length: {len(key)*8} bits")
    return mac


def verify_auth_tag(message, key, received_mac):
    mac = hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(mac, received_mac):
        print("MAC verification successful")
        return True
    else:
        print("MAC verification failed")
        return False


class WindowController:
    def __init__(self):
        self.usr_model = None
        self.main_window = None

    def add_usr_model(self, usr_model):
        self.usr_model = usr_model

    def add_window(self, main_window):
        self.main_window = main_window

    def send_money(self, user: str, amount: int, description: str): 
        message = ""
        if user == "" or amount == "" or description == "":
            
            if description == "":
                message += ("Description cannot be empty\n")

            if amount == "":
                message += ("Amount cannot be empty\n")

            if user == "":
                message += ("User cannot be empty\n")
            
            self.window.frames["Send Money"].show_message(message, "red")
            return

        if self.usr_model.balance < int(amount):
            self.window.frames["Send Money"].show_message("Insufficient funds", "red")
            return
        
        try:
            self.usr_model.new_transaction(user, amount, description)
        except IndexError: 
            self.window.frames["Send Money"].show_message("User not found", "red")
            return
        except Exception as e:
            self.window.frames["Send Money"].show_message(str(e), "red")
            return
        
        try: 
            self.usr_model.update_balance()
        except Exception as e:
            raise e
        
        self.update_home()
        self.window.frames["Send Money"].transaction_completed()

    def update_home(self):
        self.window.frames["Home"].set_data(self.usr_model)

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

    def send_money(self, user: str, amount, description: str): 
        """
        This function is called when the user wants to send money to another user.
        """

        #Check if any field is empty
        message = ""
        if user == "" or amount == "" or description == "":
            
            if description == "":
                message += ("Description cannot be empty\n")

            if amount == "":
                message += ("Amount cannot be empty\n")

            if user == "":
                message += ("User cannot be empty\n")
            
            self.window.frames["Send Money"].show_message(message, "red")
            return
        
        #Check if amount is a positive integer
        if not amount.isdigit() or int(amount) <= 0:
            self.window.frames["Send Money"].show_message("Amount must be a positive number", "red")
            return

        #Check if user has enough funds
        if self.usr_model.balance < int(amount):
            self.window.frames["Send Money"].show_message("Insufficient funds", "red")
            return
        
        #Create the data string to be encrypted
        data = amount + ":" + description

        #Ask the model to create a new transaction
        try:
            self.usr_model.new_transaction(user, data)
        except IndexError: 
            self.window.frames["Send Money"].show_message("User not found", "red")
            return
        except Exception as e:
            self.window.frames["Send Money"].show_message(str(e), "red")
            return
        
        #If everything was successful, update the balance and the home frame
        try: 
            self.usr_model.update_balance()
        except Exception as e:
            raise e
        
        #Update the home frame and show a success message
        self.update_home()
        self.window.frames["Send Money"].transaction_completed()

    def update_home(self):
        self.window.frames["Home"].set_data(self.usr_model)

        





