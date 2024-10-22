from supabase import create_client, Client

supabase_url = "https://ldbsmswgtwtkxduqmoip.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkYnNtc3dndHd0a3hkdXFtb2lwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk2MDI5ODEsImV4cCI6MjA0NTE3ODk4MX0.7GndoQP5VHZx1dAfMwcLMlmJjwUcEsFMsuZLv77mG0k"
supabase: Client = create_client(supabase_url, supabase_key)
from supabase import create_client, Client
import bcrypt
import pyotp
import os
import hmac
import hashlib
import logging

# Initialize Supabase client
supabase_url = "YOUR_SUPABASE_URL"
supabase_key = "YOUR_SUPABASE_API_KEY"
supabase: Client = create_client(supabase_url, supabase_key)

# Configure logging
logging.basicConfig(filename='auth_log.log', level=logging.DEBUG,
                    format='%(asctime)s - %(message)s')

# Function to generate hashed password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to generate OTP secret
def generate_otp_secret() -> str:
    return pyotp.random_base32()

# Function to send OTP (for now, we'll just print it)
def send_otp_email(email: str, otp: str):
    print(f"Sending OTP: {otp} to {email}")

# Register a new user
def register_user(email: str, password: str):
    # Hash the user's password
    hashed_password = hash_password(password)

    # Generate OTP secret for 2FA
    otp_secret = generate_otp_secret()
    totp = pyotp.TOTP(otp_secret)
    otp = totp.now()

    # Insert user into the database
    response = supabase.table('users').insert({
        "email": email,
        "password_hash": hashed_password,
        "otp_secret": otp_secret
    }).execute()

    if response.get('status_code') == 201:
        send_otp_email(email, otp)
        logging.debug(f'User {email} registered with hashed password and OTP sent')
    else:
        logging.error(f"Error registering user: {response}")

# Function to generate HMAC for message authentication
def generate_hmac(message: str, secret_key: str, algorithm: str = 'sha256') -> str:
    secret_key_bytes = secret_key.encode('utf-8')
    message_bytes = message.encode('utf-8')

    # Select hashing algorithm
    if algorithm == 'sha256':
        hash_function = hashlib.sha256
    elif algorithm == 'sha512':
        hash_function = hashlib.sha512
    else:
        raise ValueError("Unsupported algorithm. Choose from: sha256, sha512.")

    hmac_obj = hmac.new(secret_key_bytes, message_bytes, hash_function)
    hmac_digest = hmac_obj.hexdigest()

    # Log the result
    key_length = len(secret_key_bytes) * 8  # bits
    logging.debug(f'HMAC generated: {hmac_digest} | Algorithm: {algorithm} | Key length: {key_length} bits')

    return hmac_digest

# Function to verify HMAC
def verify_hmac(message: str, received_hmac: str, secret_key: str, algorithm: str = 'sha256') -> bool:
    calculated_hmac = generate_hmac(message, secret_key, algorithm)
    is_valid = hmac.compare_digest(calculated_hmac, received_hmac)

    # Log verification result
    if is_valid:
        logging.debug(f'HMAC verification successful for message: "{message}"')
    else:
        logging.debug(f'HMAC verification failed for message: "{message}"')

    return is_valid

# Example usage
if __name__ == '__main__':
    # Register a user
    email = "user@example.com"
    password = "strongpassword123"
    register_user(email, password)

    # Example message authentication
    message = "Sensitive banking transaction"
    secret_key = os.urandom(32).hex()  # Generate a random secret key
    hmac_value = generate_hmac(message, secret_key)
    print(f"Generated HMAC: {hmac_value}")

    # Verify the HMAC
    is_valid = verify_hmac(message, hmac_value, secret_key)
    print(f"HMAC verification valid: {is_valid}")
