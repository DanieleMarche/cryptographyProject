from Cryptography.cryptography_utils import text_hash, equals
from DataBase.database_utils import get_hashed, user_login


class UserModel:

    def __init__(self, username, password, secret_code):
        response = user_login(username, password, secret_code)
        if response:
            self.username = response["email"]
            self.name = response["name"]
            self.surname = response["surname"]
            self.balance = response["money"]
            self.date_of_birth = response["birthday"]
        else:
            raise ValueError("Invalid credentials")


