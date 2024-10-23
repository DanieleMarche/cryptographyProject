import os
import json

from Cryptography.cryptography_utils import text_hash, equals
from DataBase.database_utils import get_hashed, user_login, update_database


class UserModel:

    def __init__(self, username, password, secret_code):
        response = user_login(username, password, secret_code)
        if response:
            self.username = response["email"]
            self.name = response["name"]
            self.surname = response["surname"]
            self.balance = response["money"]
            self.date_of_birth = response["birthday"]
            self.touch_id = response["touch_id"]
            self.touch_id_device = response["touch_id_device"]
        else:
            raise ValueError("Invalid credentials")

    def save_user_data(self):
        try:
            update_database(self.username, self.touch_id, self.touch_id_device)

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





