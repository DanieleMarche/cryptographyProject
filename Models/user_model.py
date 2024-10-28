import os
import json
import pytz

from datetime import datetime
from DataBase.database_utils import *


class UserModel:

    def __init__(self, username, password, secret_code):
        try:
            response = user_login(username, password, secret_code)
            print(response)
            if response:
                self.username = response["email"]
                self.name = response["name"]
                self.surname = response["surname"]
                self.balance = response["money"]
                self.date_of_birth = response["birthday"]
                self.touch_id = response["touch_id"]
                self.touch_id_device = response["touch_id_device"]
                a = response["last_balance_update"]
                print(response["last_balance_update"])
                self.last_balance_update = datetime.fromisoformat(a)

                
                self.transactions = get_transactions(self.username)
                
                if datetime.fromisoformat(self.transactions[-1]["created_at"]) > self.last_balance_update:
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
        
    def new_transaction(self, user: str, amount: int, description: str): 
        try:
            user_public_key = get_user_public_key(user)
            #encryption will be implemented later
            add_transaction(self.username, user, amount, description)
            
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
            self.transactions = get_transactions(self.username)
            for transaction in self.transactions:
                if datetime.fromisoformat(transaction["created_at"]) > self.last_balance_update:
                    if transaction["user1"] == self.username:
                        self.balance -= transaction["money"]
                    else:
                        self.balance += transaction["money"]  

            upadate_balance(self.username, self.balance)
        except Exception as e:
            raise e
        


    # Inside UserModel
    def create_user(self, password, secret_code):
        new_user = {'username': self.username, 'password': password, 'secret_code': secret_code}
        with open('user_data.json', 'a') as file:
            json.dump(new_user, file)
        return new_user




