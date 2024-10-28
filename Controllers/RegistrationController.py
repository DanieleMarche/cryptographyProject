import bcrypt
import secrets
import json


class RegistrationController:
    def __init__(self):
        self.view = None


    def register(self, username, password, secret_code, fingerprint_placeholder="dummy_biometric"):
        # 1. Password Hashing
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # 2. Token Authentication (Simulating SMS or App token)
        token = secrets.token_hex(16)  # Example token generation

        # 3. Store Biometric Mock (Fingerprint Placeholder)
        user_data = {
            "username": username,
            "password_hash": hashed_password.decode(),
            "secret_code": secret_code,
            "token": token,
            "fingerprint": fingerprint_placeholder  # This should ideally be a hash of biometric data
        }

        # Save user data securely
        with open(f"{username}_credentials.json", "w") as file:
            json.dump(user_data, file)

        print(f"User {username} registered with token {token}")

        self.view.show_message("Registration successful!")

    def add_view(self, view):
        self.view = view

