import hashlib
import uuid
import ast
import logging
import os
import subprocess
import locale 
import requests

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from pathlib import Path

logging.basicConfig(filename= "Documents/myBank.log", level=logging.INFO)

class Transaction():
    def __init__(self, user1, user2, user1_aes_key, user2_aes_key, aes_nounce, tag, data, sign, cert, cert_chain, created_at):
        self.user1 = user1
        self.user2 = user2
        
        if user1_aes_key.__class__ != bytes:
            self.user1_aes_key = ast.literal_eval(user1_aes_key)
        else:
            self.user1_aes_key = user1_aes_key

        if user2_aes_key.__class__ != bytes:
            self.user2_aes_key = ast.literal_eval(user2_aes_key)
        else:
            self.user2_aes_key = user2_aes_key

        if aes_nounce.__class__ != bytes:
            self.aes_nounce = ast.literal_eval(aes_nounce)
        else:
            self.aes_nounce = aes_nounce

        if tag.__class__ != bytes:
            self.tag = ast.literal_eval(tag)
        else:
            self.tag = tag

        if data.__class__ != bytes:
            self.enc_data = ast.literal_eval(data)
        else:
            self.enc_data = data
        
        if sign.__class__ != bytes:
            self.sign = ast.literal_eval(sign)
        else:
            self.sign = sign
        
        if cert.__class__ != bytes:
            self.cert = ast.literal_eval(cert)
        else:
            self.cert = cert
        
        if cert_chain.__class__ != bytes:
            self.cert_chain = ast.literal_eval(cert_chain)
        else:
            self.cert_chain = cert_chain
        
        self.created_at = created_at
        
        self.amount = None
        self.description = None


def text_hash(encoded_text: bytes) -> str:
    return hashlib.sha512(encoded_text).hexdigest()

def equals(clear_text: str, hashed_text: str) -> bool:
    return text_hash(clear_text) == hashed_text

def generate_salt():
    return get_random_bytes(16)

def get_mac_address():
    mac = uuid.getnode()
    mac_address = ':'.join(['{:02x}'.format((mac >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])
    return mac_address

def generate_rsa_keys(secret_code: str):
    """
    Generates RSA key pair and saves the private key to a file.
    Args:
        secret_code (str): The passphrase used to encrypt the private key.
    Returns:
        bytes: The public key in PEM format.
    The private key is saved to 'Documents/rsa_key.bin' with PKCS#8 and 
    scryptAndAES128-CBC protection.
    """
    key = RSA.generate(2048)

    private_key = key.export_key(passphrase=secret_code)
    encrypted_key = key.export_key(passphrase=secret_code, pkcs=8,
                              protection="scryptAndAES128-CBC",
                              prot_params={'iteration_count':131072})

    with open("Documents/rsa_key.bin", "wb") as f:
        f.write(encrypted_key)

    public_key = key.publickey().export_key()

    logging.info("Generated RSA keys 2048 bits long" )

    return public_key

def encrypt_rsa_transaction(user1_public_key: str, user2_public_key: str, transaction: Transaction) -> Transaction:
    """
    Encrypts data using RSA and AES in GCM mode.
    """

    user1_recipient_key = RSA.import_key(user1_public_key)
    user2_recipient_key = RSA.import_key(user2_public_key)
    session_key = get_random_bytes(16)

    # Encrypt the session key with RSA public keys
    user1_cipher_rsa = PKCS1_OAEP.new(user1_recipient_key)
    user1_enc_session_key = user1_cipher_rsa.encrypt(session_key)
    user2_cipher_rsa = PKCS1_OAEP.new(user2_recipient_key)
    user2_enc_session_key = user2_cipher_rsa.encrypt(session_key)

    # Encrypt data with AES in GCM mode
    cipher_aes = AES.new(session_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(transaction.enc_data)

    # Transaction datas replaced with encrypted data
    transaction.enc_data = ciphertext

    # Encryption information added to the transaction
    transaction.user1_aes_key = user1_enc_session_key
    transaction.user2_aes_key = user2_enc_session_key
    transaction.tag = tag
    transaction.aes_nounce = cipher_aes.nonce

    # Updating the log 
    logging.info("Data encrypted using AES-GCM with 128-bit session key.")
    
    return transaction

def decrypt_rsa(encrypted_transaction: Transaction, passphrase: str, role: int) -> Transaction:
    """
    Decrypts an RSA encrypted transaction using the provided passphrase and role.

    Args:
        encrypted_transaction (Transaction): The transaction object containing encrypted data.
        passphrase (str): The passphrase to unlock the private RSA key.
        role (int): The role of the user (1 or 2) to determine which AES key to use.

    Returns:
        Transaction: The decrypted transaction object with the data field populated.

    Raises:
        ValueError: If the passphrase is invalid or if authentication fails.
    """

    # Load the private RSA key
    try:
        private_key = RSA.import_key(open("Documents/rsa_key.bin").read(), passphrase=passphrase)
    except ValueError:
        logging.error("Invalid passphrase provided for decrypt data.")
        raise ValueError("Invalid passphrase")

    # Choose the ancrypted session key based on the role of the
    enc_session_key = (encrypted_transaction.user1_aes_key if role == 1 else
                       encrypted_transaction.user2_aes_key)

    nonce = encrypted_transaction.aes_nounce
    tag = encrypted_transaction.tag
    ciphertext = encrypted_transaction.enc_data

    # Decrypt session key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt data and verify authenticity
    cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce)
    try:
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        logging.info("Data decryption and authentication successful using AES-GCM.")
    except ValueError:
        logging.error("Authentication failed. Data integrity compromised.")
        raise ValueError("Authentication failed")

    # Returns the transaction with the dec text on the dec_data field 
    dec_transaction = encrypted_transaction

    data.decode('utf-8')
    data.split(":")

    try: 
        dec_transaction.amount = data[0]
        dec_transaction.description = data[1]
    except IndexError: 
        raise IndexError("Problem fetching datas")

    return dec_transaction

def is_correct_passkey(passkey: str) -> bool:
    """
    Checks if the provided passkey is correct for decrypting the private RSA key stored in 'Documents/rsa_key.bin'.
    :param passkey: The passphrase to check
    :return: True if the passkey is correct, False otherwise
    """
    try:
        RSA.import_key(open("Documents/rsa_key.bin").read(), passphrase=passkey)
        logging.info("Correct passkey provided.")
        return True
    except (ValueError, IndexError):
        logging.error("Invalid passkey provided.")
        return False
    
def key_derivation_user_data(passphrase: str, salt: bytes) -> bytes:
    """
    Derives a key from the passphrase using PBKDF2.
    :param passphrase: The passphrase to derive the key from
    :param salt: The salt to use in the key derivation
    :return: The derived key
    """
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, 100000, 32)

def derive_key_certificate(passphrase: str, salt: bytes, n: int = 16384, r: int = 8, p: int = 1, dklen: int = 32) -> bytes:
    """
    Derives a cryptographic key using the scrypt function.

    Args:
        passphrase (str): The passphrase to use for key derivation.
        salt (bytes): A unique salt to ensure secure derivation.
        n (int): Cost factor (must be a power of 2, e.g., 16384).
        r (int): Block size parameter.
        p (int): Parallelism factor.
        dklen (int): Desired length of the derived key in bytes (default 32).

    Returns:
        bytes: The derived key as a byte sequence.

    Raises:
        ValueError: If the parameters are invalid.
    """
    try:
        derived_key = hashlib.scrypt(
            passphrase.encode('utf-8'),  # Convert the passphrase to bytes
            salt=salt,
            n=n,
            r=r,
            p=p,
            dklen=dklen
        )
        return derived_key
    except ValueError as e:
        raise ValueError(f"Error in key derivation: {e}")

def aes_encrypt(data: str, key: bytes) -> bytes:
    """
    Encrypts data using AES in CBC mode.
    :param data: The data to encrypt
    :param key: The key to use for encryption
    :return: The encrypted data
    """
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    padded_data = data + (16 - len(data) % 16) * chr(16 - len(data) % 16)
    ciphertext = cipher.encrypt(padded_data.encode())
    logging.info("Encrypted AES CBC with key 16 bytes long")
    return iv + ciphertext

def aes_decrypt(ciphertext: bytes, key: bytes) -> str:
    """
    Decrypts data using AES in CBC mode.
    :param ciphertext: The encrypted data
    :param key: The key to use for decryption
    :return: The decrypted data
    """
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = cipher.decrypt(ciphertext).decode()
    padding_length = ord(padded_data[-1])
    logging.info("Decrypted AES CBC with key 16 bytes long")
    return padded_data[:-padding_length]

def get_location_data():
    """
    Retrieves location data (country, state, city) based on the public IP address.
    
    Returns:
        dict: A dictionary with keys 'country', 'state', and 'city'.
    """
    try:
        response = requests.get("http://ip-api.com/json/")
        response.raise_for_status()
        data = response.json()

        if data["status"] == "success":
            return {
                "country": data.get("countryCode", "Unknown"),
                "state": data.get("regionName", "Unknown"),
                "city": data.get("city", "Unknown")
            }
        else:
            raise ValueError("Could not retrieve location data.")
    except Exception as e:
        print(f"Error fetching location data: {e}")
        return {"country": "Unknown", "state": "Unknown", "city": "Unknown"}


def generate_openssl_config(mail: str, name: str, surname: str, org="MyBank", unit="IT"):
    """
    Generates an OpenSSL configuration file for CSR generation.
    Automatically retrieves location data (country, state, city) based on IP.

    Args:
        mail (str): Email of the user (used for CN and emailAddress).
        org (str): Organization name (default is 'MyOrganization').
        unit (str): Organizational unit name (default is 'MyUnit').

    Returns:
        str: Path to the generated configuration file.
    """
    if not mail:
        raise ValueError("Email address is required.")
    
    # Get location data
    location = get_location_data()
    country = location["country"]
    state = location["state"]
    city = location["city"]

    config_content = f"""
[ req ]
default_bits        = 2048
default_md          = sha256
distinguished_name  = req_distinguished_name
prompt              = no

[ req_distinguished_name ]
C                   = {country}
ST                  = {state}
L                   = {city}
O                   = {org}
OU                  = {unit}
CN                  = {name + " " + surname}
emailAddress        = {mail}
"""
    # Directory to save the configuration file
    config_dir = Path("Documents")

    # File path
    config_file_path = config_dir / f"{mail}_openssl.cnf"

    # Write the configuration file
    with open(config_file_path, "w") as config_file:
        config_file.write(config_content)
    
    print(f"OpenSSL configuration file generated: {config_file_path}")
    return str(config_file_path)

def generate_rsa_key_and_csr_using_config(mail: str, passphrase: str, config_file_path: str) -> str:
    """
    Generates an RSA key and a CSR using an existing OpenSSL configuration file.

    Args:
        mail (str): Email of the user (used for CN and emailAddress).
        passphrase (str): The passphrase for securing the private key.
        config_file_path (str): Path to the OpenSSL configuration file (.cnf).

    Returns:
        str: Path to the generated CSR file.
    """
    # Check if the config file exists
    config_file = Path(config_file_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file '{config_file_path}' does not exist.")
    
    # Paths for the key and CSR
    key_file = f"{mail}_key.pem"
    csr_file = f"{mail}_req.pem"
    
    try:
        # Generate the RSA key and CSR using the configuration file
        subprocess.run([
            "openssl", "req", "-newkey", "rsa:2048", "-days", "360", "-sha256",
            "-keyout", "Documents/" + key_file, "-out", "Documents/" + csr_file, "-passout", f"pass:{passphrase}",
            "-config", config_file_path
        ], check=True)

        logging.info(f"RSA key saved as: {key_file}")
        logging.info(f"CSR saved as: {csr_file}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error while executing OpenSSL: {e}")
        raise
    except Exception as e:
        print(f"General Error: {e}")
        raise
    
    return str(Path("Documents") / csr_file)

def send_cert_req(ca: str, req_path: str):
    """
    Moves the certificate request file to the specified CA directory.

    Args:
        ca (str): The path to the CA directory.
        req_path (str): The path to the certificate request file.

    Returns:
        None
    """
    try:
        # Ensure the CA directory exists
        base_dir = Path("Gerarquia_CAs/end_point_cas")
        ca_dir = base_dir / ca
        if not ca_dir.exists():
            raise FileNotFoundError(f"CA directory '{ca_dir}' does not exist.")

        # Move the request file to the CA directory
        req_file = Path(req_path)
        if req_file.exists():
            destination = ca_dir / "solicitudes" / req_file.name
            req_file.rename(destination)
            logging.info(f"Moved certificate request file to: {destination}")
        else:
            raise FileNotFoundError(f"Request file '{req_path}' does not exist.")
    except Exception as e:
        logging.error(f"Error moving certificate request file: {e}")
        raise