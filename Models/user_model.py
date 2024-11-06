import os
import json
import ast
import logging

from datetime import datetime
from DataBase.database_utils import *

logging.basicConfig(filename= "Documents/myBank.log", level=logging.INFO)

class UserModel:

    def __init__(self, username, password, secret_code):
        try:
            response = self.user_login(username, password, secret_code)
            
            if response:
                self.username = response["email"]
                user_data = ast.literal_eval(response["user_data"])
                user_data_salt = ast.literal_eval(response["salt_aes"])

                ke = kdf(password, user_data_salt)

                self.user_data = aes_decrypt(user_data, ke)
                

                self.balance = response["money"]
                self.touch_id = response["touch_id"]
                self.touch_id_device = response["touch_id_device"]
                self.public_key = response["public_key"]
                self.secret_code = secret_code
                a = response["last_balance_update"]
                print(response["last_balance_update"])
                self.last_balance_update = datetime.fromisoformat(a)
                
                enc_transactions = get_transactions(self.username)

                self.transactions = self.decrypt_transactions(enc_transactions, self.secret_code)
                    
                if len(self.transactions) > 0 and datetime.fromisoformat(self.transactions[-1]["created_at"]) > self.last_balance_update:
                    self.update_balance()

        except ValueError as e:
            print(e)
            raise ValueError("Invalid credentials")
        except Exception as e:
            print(e)
            raise e

    def save_user_data(self):
        try:
            update_touch_id(self.username, self.touch_id, self.touch_id_device)

            # Se touch_id è True, aggiorna il file "remember_user.json"
            if self.touch_id:
                remember_file_path = "Documents/remember_user.json"

                # Carica il contenuto del file se esiste
                if os.path.exists(remember_file_path):
                    with open(remember_file_path, 'r') as f:
                        data = json.load(f)
                else:
                    data = {}

                # Aggiorna il campo "email" nel file JSON
                data["email"] = self.email

                # Salva le modifiche nel file
                with open(remember_file_path, 'w') as f:
                    json.dump(data, f, indent=4)

        except Exception as e:
            raise e
        
    def new_transaction(self, receiver: str, data: str): 
        try:
            receiver_public_key = get_user_public_key(receiver)["public_key"]
        except Exception as e: 
            raise e

        try:
            add_transaction(self.username, self.public_key, receiver, receiver_public_key,  data)
            
        except Exception as e:
            raise e
        
    def update_balance(self):
        """
        Updates the user's balance based on recent transactions and a specified amount.
        This method retrieves all transactions associated with the user's username and updates the balance
        by iterating through each transaction. If the transaction date is more recent than the last balance update,
        it adjusts the balance accordingly. After processing the transactions, it updates the balance with the given amount.
        Args:
            amount (int): The amount to update the balance with.
        Raises:
            Exception: If an error occurs during the balance update process.
        """

        try:
            self.transactions = self.decrypt_transactions(get_transactions(self.username), self.secret_code)
            for transaction in self.transactions:
                if datetime.fromisoformat(transaction["created_at"]) > self.last_balance_update:
                    if transaction["user1"] == self.username:
                        self.balance -= int(transaction["amount"])
                    else:
                        self.balance += int(transaction["amount"])

            upadate_balance(self.username, self.balance)
        except Exception as e:
            raise e
        
    def decrypt_transactions(self, enc_transactions: list, secret_code) -> list[dict]: 
        """
        This function decrypt every transaction. 
        """
        dec_transactions = []
        for enc_transaction in enc_transactions: 
            if enc_transaction["user1"] == self.username: role = 1
            else: role = 2

            dec_data = decrypt_rsa(enc_transaction["encrypted_transaction"], secret_code, role)

            data = dec_data.split(":")

            dec_transaction = {
                "user1" : enc_transaction["user1"],
                "user2" : enc_transaction["user2"],
                "created_at" : enc_transaction["created_at"],
                "amount" : data[0],
                "description" : data[1]
                }
            
            dec_transactions.append(dec_transaction)

        return dec_transactions

    # Inside UserModel
    @staticmethod
    def create_user(user_data: dict):
        try:
            new_row(user_data)
        except Exception as e:
            raise e
    
    @staticmethod
    def user_login(usr: str, psw: str, secret_code: str):
        if not is_correct_passkey(secret_code): 
            raise Exception("Invalid secret code.")
        
        if psw == "": 
            data = {
            "select": "email, touch_id, touch_id_device",
            "email": f"eq.{usr}",
            }

            response = requests.get(user_url, headers=headers, params=data)

            if response.status_code == 200:
                result = response.json()
                result = result[0]
                if result and result["touch_id"] == True and result["touch_id_device"] == get_mac_address():
                    if authenticate(): 
                        return get_user_data(usr)
                else: 
                    raise Exception("Touch ID not enabled or not available on this device")
                
            else:
                raise Exception("Server error")
        else: 

            hashed_psw, salt = get_hashed(usr)
            if equals(psw.encode() + ast.literal_eval(salt), hashed_psw):
                return get_user_data(usr)




