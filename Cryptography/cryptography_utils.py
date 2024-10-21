import hashlib

def password_hash(psw: str) -> str:
    return hashlib.sha512(psw.encode()).hexdigest()

def password_check(psw: str, hashed_psw: str) -> bool:
    return password_hash(psw) == hashed_psw

