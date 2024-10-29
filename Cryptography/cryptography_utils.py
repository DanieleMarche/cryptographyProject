import hashlib
import uuid
import ast
import logging

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

logging.basicConfig(filename= "Documents/myBank.log", level=logging.INFO)

class EncryptedTransaction():
    def __init__(self, user1_aes_key, user2_aes_key, aes_nounce, tag, cyphertext):
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

        if cyphertext.__class__ != bytes:
            self.cyphertext = ast.literal_eval(cyphertext)
        else:
            self.cyphertext = cyphertext

    def __str__(self):
        return f"user1_aes_key: {self.user1_aes_key}, user2_aes_key: {self.user2_aes_key}, aes_nounce: {self.aes_nounce}, tag: {self.tag}, cyphertext: {self.cyphertext}"

    def __repr__(self):
        return f"user1_aes_key: {self.user1_aes_key}, user2_aes_key: {self.user2_aes_key}, aes_nounce: {self.aes_nounce}, tag: {self.tag}, cyphertext: {self.cyphertext}" 


def text_hash(encoded_text: bytes) -> str:
    return hashlib.sha512(encoded_text).hexdigest()

def equals(clear_text: str, hashed_text: str) -> bool:
    return text_hash(clear_text) == hashed_text

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

from typing import Tuple

def encrypt_rsa_transaction(user1_public_key: str, user2_public_key: str, data: str) -> EncryptedTransaction:
    """
    Encrypts data using RSA and AES in GCM mode.
    """
    data = data.encode("utf-8")

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
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    logging.info("Data encrypted using AES-GCM with 128-bit session key.")
    return EncryptedTransaction(user1_enc_session_key, user2_enc_session_key, cipher_aes.nonce, tag, ciphertext)

def decrypt_rsa(encrypted_data: EncryptedTransaction, passphrase: str, role: int) -> str:
    """
    Decrypts data using RSA and AES in GCM mode.
    """
    # Load the private RSA key
    try:
        private_key = RSA.import_key(open("Documents/rsa_key.bin").read(), passphrase=passphrase)
    except ValueError:
        logging.error("Invalid passphrase provided for decrypt data.")
        raise ValueError("Invalid passphrase")

    enc_session_key = (encrypted_data.user1_aes_key if role == 1 else
                       encrypted_data.user2_aes_key)

    nonce = encrypted_data.aes_nounce
    tag = encrypted_data.tag
    ciphertext = encrypted_data.cyphertext

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

    return data.decode("utf-8")

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
    
