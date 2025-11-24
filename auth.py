"""Simple authentication helpers.

Provides:
- `hash_password(password)` -> (salt: bytes, hash: bytes)
- `verify_password(password, salt, hash)` -> bool
- `generate_token(nbytes=32)` -> str

Uses PBKDF2-HMAC-SHA256 for password hashing and `secrets` for token generation.
"""

import hashlib
import hmac
import secrets
from typing import Tuple


def hash_password(password: str, salt: bytes | None = None, iterations: int = 100_000) -> Tuple[bytes, bytes]:
    """Hash a password with PBKDF2-HMAC-SHA256.

    Returns a tuple `(salt, hash)` where both are bytes. If `salt` is None a
    new 16-byte salt will be generated.
    """
    if salt is None:
        salt = secrets.token_bytes(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return salt, pwd_hash


def verify_password(password: str, salt: bytes, pwd_hash: bytes, iterations: int = 100_000) -> bool:
    """Verify a password against `salt` and `pwd_hash`.

    Uses `hmac.compare_digest` to avoid timing attacks.
    """
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(new_hash, pwd_hash)


def generate_token(nbytes: int = 32) -> str:
    """Generate a URL-safe token string with `nbytes` of entropy."""
    return secrets.token_urlsafe(nbytes)


if __name__ == "__main__":
    # Quick demo when run directly
    s, h = hash_password("password123")
    print("salt:", s.hex())
    print("hash:", h.hex())
    print("verify:", verify_password("password123", s, h))
    print("token:", generate_token())
