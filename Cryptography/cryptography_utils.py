import hashlib

def text_hash(text: str) -> str:
    return hashlib.sha512(text.encode()).hexdigest()


def equals(clear_text: str, hashed_text: str) -> bool:
    return text_hash(clear_text) == hashed_text

