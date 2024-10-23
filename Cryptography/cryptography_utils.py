import hashlib
import uuid

def text_hash(text: str) -> str:
    return hashlib.sha512(text.encode()).hexdigest()


def equals(clear_text: str, hashed_text: str) -> bool:
    return text_hash(clear_text) == hashed_text

def get_mac_address():
    mac = uuid.getnode()
    mac_address = ':'.join(['{:02x}'.format((mac >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])
    return mac_address
