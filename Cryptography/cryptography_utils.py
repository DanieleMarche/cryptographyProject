import hashlib
import uuid
import ast

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

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



def text_hash(text: str) -> str:
    return hashlib.sha512(text.encode()).hexdigest()


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

    with open("Documents/rsa_key_mario.bin", "wb") as f:
        f.write(encrypted_key)

    public_key = key.publickey().export_key()

    return public_key

from typing import Tuple

def encrypt_rsa_transaction(user1_public_key: str, user2_public_key: str, data: str) -> EncryptedTransaction:
    """
    This function uses code from the PyCryptodome library and docs to encrypt data using RSA.
    This function encrypts the AES key using the RSA public key of both users of the transaction
    so that both can decrypt the data in the future.
    :param user1_public_key: The public RSA key of user 1
    :param user2_public_key: The public RSA key of user 2
    :param data: The data to encrypt
    :return: A dictionary containing the encrypted session keys, nonce, tag, and ciphertext
    """

    data = data.encode("utf-8")

    user1_recipient_key = RSA.import_key(user1_public_key)
    user2_recipient_key = RSA.import_key(user2_public_key)

    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    user1_cipher_rsa = PKCS1_OAEP.new(user1_recipient_key)
    user1_enc_session_key = user1_cipher_rsa.encrypt(session_key)

    user2_cipher_rsa = PKCS1_OAEP.new(user2_recipient_key)
    user2_enc_session_key = user2_cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    return EncryptedTransaction(user1_enc_session_key, user2_enc_session_key, cipher_aes.nonce, tag, ciphertext)



def decrypt_rsa(encrypted_data: EncryptedTransaction, passphrase: str, role: int) -> str:
    """
    This function uses code from the PyCryptodome library and docs to decrypt data using RSA.
    :param encrypted_data: The dictionary containing encrypted session key, nonce, tag, and ciphertext
    :param passphrase: The passphrase to decrypt the private RSA key
    :param role: The role of the user in the transaction, 1 for sender, 2 for receiver
    """

    # Load the private RSA key, if the passphrase is incorrect, raise a ValueError
    try: 
        private_key = RSA.import_key(open("Documents/rsa_key.bin").read(), passphrase=passphrase)
    except ValueError:
        raise ValueError("Invalid passphrase")

    # Get the encrypted session key, nonce, tag, and ciphertext from the dictionary
    if role == 1:
        enc_session_key = encrypted_data.user1_aes_key
    elif role == 2:
        enc_session_key = encrypted_data.user2_aes_key
    else: 
        raise ValueError("Invalid role")
    
    nonce = encrypted_data.aes_nounce
    tag = encrypted_data.tag
    ciphertext = encrypted_data.cyphertext

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    return data.decode("utf-8")

def is_correct_passkey(passkey: str) -> bool:
    """
    Checks if the provided passkey is correct for decrypting the private RSA key stored in 'Documents/rsa_key.bin'.
    :param passkey: The passphrase to check
    :return: True if the passkey is correct, False otherwise
    """
    try:
        RSA.import_key(open("Documents/rsa_key.bin").read(), passphrase=passkey)
        return True
    except (ValueError, IndexError):
        return False