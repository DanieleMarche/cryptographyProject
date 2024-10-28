import hashlib
import uuid

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


def text_hash(text: str) -> str:
    return hashlib.sha512(text.encode()).hexdigest()


def equals(clear_text: str, hashed_text: str) -> bool:
    return text_hash(clear_text) == hashed_text

def get_mac_address():
    mac = uuid.getnode()
    mac_address = ':'.join(['{:02x}'.format((mac >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])
    return mac_address

def generate_rsa_keys(secret_code: str):
    key = RSA.generate(2048)

    private_key = key.export_key(passphrase=secret_code)
    encrypted_key = key.export_key(passphrase=secret_code, pkcs=8,
                              protection="scryptAndAES128-CBC",
                              prot_params={'iteration_count':131072})

    with open("Documents/rsa_key.bin", "wb") as f:
        f.write(encrypted_key)

    public_key = key.publickey().export_key()

    return public_key

def encrypt_rsa(public_key: str, data: str) -> bytes:

    data = data.encode("utf-8")
    """
    This function uses code from the PyCryptodome library and docs to encrypt data using RSA.
    :param public_key: The public RSA key
    """

    recipient_key = RSA.import_key(public_key)
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key

    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    return {"aes": enc_session_key, "aes_nounce" : cipher_aes.nonce, "tag": tag, "cyphertext": ciphertext}

def decrypt_rsa(encrypted_data: dict, passphrase: str) -> str:
    """
    This function uses code from the PyCryptodome library and docs to decrypt data using RSA.
    :param encrypted_data: The dictionary containing encrypted session key, nonce, tag, and ciphertext
    :param passphrase: The passphrase to decrypt the private RSA key
    """
    private_key = RSA.import_key(open("Documents/rsa_key.bin").read(), passphrase=passphrase)

    enc_session_key = encrypted_data["aes"]
    nonce = encrypted_data["aes_nounce"]
    tag = encrypted_data["tag"]
    ciphertext = encrypted_data["cyphertext"]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    return data.decode("utf-8")