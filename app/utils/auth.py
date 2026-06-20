import os
import uuid
import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import bcrypt

# Secret keys for JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key-change-in-production-123456")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against its hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Generates a password hash from plain text password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a short-lived JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def generate_refresh_token() -> str:
    """Generates a secure, random refresh token string."""
    return os.urandom(32).hex()

def generate_temp_password(first_name: str) -> str:
    """
    Generates a password containing:
    1. First 4 characters of first_name (lowercased)
    2. 4 random alphanumeric characters
    """
    clean_name = "".join(c for c in first_name if c.isalpha()).lower()
    prefix = clean_name[:4] if len(clean_name) >= 4 else clean_name.ljust(4, "x")
    
    random_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{prefix}{random_part}"
