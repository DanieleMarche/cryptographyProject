import hmac
import hashlib


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
        





