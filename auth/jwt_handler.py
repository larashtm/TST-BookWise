# auth/jwt_handler.py
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt, JWTError
import uuid

# NOTE: untuk tugas, hardcode boleh. Di produksi pindahkan ke env var.
SECRET_KEY = "CHANGE_THIS_SECRET_KEY_BOOKWISE_2025"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 jam

def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload: Dict[str, object] = {
        "sub": str(subject),
        "role": role,
        "iat": now,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# simple refresh token utils (in-memory store handled in auth_router)
def create_refresh_token() -> str:
    # just a unique string (UUID)
    return str(uuid.uuid4())
