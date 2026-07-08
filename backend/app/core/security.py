from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import JWTError
from jose import jwt

from passlib.context import CryptContext

from backend.app.core.config import settings

# Password Hashing

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# -------------------------
# Hash Password
# -------------------------

def hash_password(password: str)->str:

    return pwd_context.hash(password)

# -------------------------
# Verify Password
# -------------------------

def verify_password(
    plain_password,
    hashed_password
)->bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# -------------------------
# Create JWT Token
# -------------------------

def create_access_token(
    data: dict
)->str:

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

# -------------------------
# Decode JWT Token
# -------------------------

def decode_access_token(
    token: str
)->dict | None:

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        return payload

    except JWTError:

        return None