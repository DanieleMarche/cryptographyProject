from Cryptography.cryptography_utils import password_hash, password_check
from DataBase.database_utils import get_hashed_pwd, user_login


class UserModel:

    def __init__(self, username, password):
        response = user_login(username, password)
        if response:
            self.username = response["email"]
            self.name = response["name"]
            self.surname = response["surname"]
            self.balance = response["money"]
            self.date_of_birth = response["birthday"]
        else:
            raise ValueError("Invalid credentials")


