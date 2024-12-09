import secrets
import json
import os 
import subprocess

from Cryptography.cryptography_utils import *
from Models.user_model import UserModel
from tkinter import messagebox
from datetime import datetime



class RegistrationController:
    def _init_(self):
        self.view = None

    def register(self, username: str, password: str, first_name: str, last_name: str, ca: str):

        try: 

            # Generation of the cnf file and getting the file path
            cnf_path = generate_openssl_config(username, first_name, last_name)

            # Generation certificate key passphrase 
            cert_psw_salt = get_random_bytes(32)
            cert_psw = derive_key_certificate(password, cert_psw_salt)

            # Generation key for signing
            key_path = generate_rsa_key_and_csr_using_config(username, cert_psw, cnf_path)

            # Sends the certificate request to the Certification Authority
            send_cert_req(ca, key_path)

            # Password Hashing
            salt = generate_salt()

            password_to_hash = password.encode() + salt # Example password hashing

            hashed_password = text_hash(password_to_hash)

            # Generate a unique code
            unique_code = secrets.token_urlsafe(12)[:16]

            rsa_public_key = generate_rsa_keys(unique_code).decode()

            kdf_salt = get_random_bytes(16)
            psw = key_derivation_user_data(password, salt=kdf_salt)

            encrypted_full_name = aes_encrypt(first_name+ " " + last_name, psw)

            user_data = {
                "email": username,
                "user_data": str(encrypted_full_name),
                "password": hashed_password,
                "salt" : str(salt),
                "touch_id": False,
                "public_key": rsa_public_key,
                "money": 0,
                "last_balance_update": datetime.now().isoformat(),
                "salt_aes": str(kdf_salt),
                "salt_sign_psw": str(cert_psw_salt)
            }
         
            UserModel.create_user(user_data)

        except Exception as e:
            self.view.show_error(str(e))
            return
        
        messagebox.showinfo("Success", f"User {username} registered with secret code {unique_code}/nPlease remember this code as it will be used for login")

    def add_view(self, view):
        self.view = view

