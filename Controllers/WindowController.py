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





