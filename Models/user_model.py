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

            #try to get the user information from the database
            response = self.user_login(username, password, secret_code)
            
            if response:
                # Assigns all of the response data to the user model

                self.username = response["email"]
                user_data = ast.literal_eval(response["user_data"])
                user_data_salt = ast.literal_eval(response["salt_aes"])

                # Decrypts user's name and surname with the key deriving fromt 
                # the user's password
                deriving_key = key_derivation_user_data(password, user_data_salt)
                self.user_data = aes_decrypt(user_data, deriving_key)
                
                self.balance = response["money"]
                self.touch_id = response["touch_id"]
                self.touch_id_device = response["touch_id_device"]
                self.public_key = response["public_key"]
                self.secret_code = secret_code
                a = response["last_balance_update"]
                
                self.last_balance_update = datetime.fromisoformat(a)
                
                # Gets the transaction and decrypts them
                enc_transactions = get_transactions(self.username)
                self.transactions = self.decrypt_transactions(enc_transactions, self.secret_code)

                # If the last transaction has happened after the last balance update, 
                # it updates the balance    
                if len(self.transactions) > 0 and datetime.fromisoformat(self.transactions[-1].created_at) > self.last_balance_update:
                    self.update_balance()

        except ValueError as e:
            print(e)
            raise ValueError("Invalid credentials")
        except Exception as e:
            print(e)
            raise e

    def save_user_data(self):
        # HAVE TO MODIFY TO SAVE ALL OF USER DATA
        # TOUCH ID FEATURE BEING DISMANTLING
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
            receiver_public_key = get_user_public_key(receiver)
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
        
    def decrypt_transactions(self, enc_transactions: list[Transaction], secret_code) -> list[Transaction]: 
        """
        Decrypts a list of encrypted transactions where the user is either the sender or the receiver.
        Args:
            enc_transactions (list): A list of encrypted transactions. Each transaction is a dictionary 
                                     containing 'user1', 'user2', 'created_at', and 'encrypted_transaction'.
            secret_code: The secret code used for RSA decryption.
        Returns:
            list[dict]: A list of decrypted transactions. Each transaction is a dictionary containing 
        """

        #the list where the deciphered transaction will be stored
        dec_transactions = []

        #loop through all of the encripted transactions
        for enc_transaction in enc_transactions: 

            #selects the role depending on whether the user is the sender or 
            #the receiver.
            #This is made to decide which encripted key to use
            if enc_transaction.user1 == self.username: role = 1
            else: role = 2

            dec_transaction = decrypt_rsa(enc_transaction, secret_code, role)
            
            dec_transactions.append(dec_transaction)

        return dec_transactions

    # Inside UserModel
    @staticmethod
    def create_user(user_data: dict):
        try:
            add_user_row(user_data)
        except Exception as e:
            raise e
    
    @staticmethod
    def user_login(usr: str, psw: str, secret_code: str):
        """
        Authenticates a user by verifying the provided username, password, and secret code.
        Args:
            usr (str): The username of the user attempting to log in.
            psw (str): The password of the user attempting to log in.
            secret_code (str): A secret code required for additional security verification.
        Raises:
            Exception: If the secret code is invalid.
        Returns:
            dict: A dictionary containing user data if authentication is successful.
        """

        #check if the secret code is right
        if not is_correct_passkey(secret_code): 
            raise Exception("Invalid secret code.")
        
        #get the hashed password and the salt from the database
        hashed_psw, salt = get_hashed(usr)

        #check if the hashed password and the hashed input password are the same
        if equals(psw.encode() + ast.literal_eval(salt), hashed_psw):
            return get_user_data(usr)




