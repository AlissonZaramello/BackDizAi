import hashlib
import secrets
import hmac

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16) 

    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000 
    )

    return f"{salt}${hash_bytes.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, password_hash = stored_hash.split("$")
    except ValueError:
        return False  

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    ).hex()

    return hmac.compare_digest(new_hash, password_hash)