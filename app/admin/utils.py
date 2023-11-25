from hashlib import sha256


def hash_password(raw_password: str) -> str:
    return sha256(raw_password.encode()).hexdigest()


def check_password(hashed_password: str, raw_password: str) -> bool:
    return hashed_password == hash_password(raw_password)
