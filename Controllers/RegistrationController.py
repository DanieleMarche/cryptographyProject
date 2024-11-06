import secrets
import json

from Cryptography.cryptography_utils import *
from Models.user_model import UserModel
from tkinter import messagebox
from datetime import datetime


class RegistrationController:
    def _init_(self):
        self.view = None


    def register(self, username, password, first_name, last_name):
        # Password Hashing
        salt = generate_salt()

        password_to_hash = password.encode() + salt # Example password hashing

        hashed_password = text_hash(password_to_hash)

        # Generate a unique code
        unique_code = secrets.token_urlsafe(12)[:16]

        rsa_public_key = generate_rsa_keys(unique_code).decode()

        kdf_salt = get_random_bytes(16)
        psw = kdf(password, salt=kdf_salt)

        en_name = aes_encrypt(first_name+ " " + last_name, psw)

        user_data = {
            "email": username,
            "user_data": str(en_name),
            "password": hashed_password,
            "salt" : str(salt),
            "touch_id": False,
            "public_key": rsa_public_key,
            "money": 0,
            "last_balance_update": datetime.now().isoformat(),
            "salt_aes": str(kdf_salt)
        }

        try: 
            UserModel.create_user(user_data)
        except Exception as e:
            self.view.show_error(str(e))
            return
        
        messagebox.showinfo("Success", f"User {username} registered with secret code {unique_code}/nPlease remember this code as it will be used for login")

    def add_view(self, view):
        self.view = view

