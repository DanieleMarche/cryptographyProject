from Cryptography.cryptography_utils import password_hash, password_check
from DataBase.database_utils import get_hashed_pwd


class UserModel:

    def __init__(self, username, password):
        if password_check(password_hash(password), get_hashed_pwd(username)):
            self.username = None
            self.name = None
            self.email = None
            self.balance = None
            self.date_of_birth = None
            #TOBEFINISHED
        else:
            raise ValueError("Wrong password or username")



