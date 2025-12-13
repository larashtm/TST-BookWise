from passlib.context import CryptContext
from uuid import UUID, uuid4
from typing import Optional, Dict

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User:
    def __init__(self, user_id: UUID, username: str, hashed_password: str, role: str, disabled: bool=False):
        self.user_id = user_id
        self.username = username
        self.hashed_password = hashed_password
        self.role = role
        self.disabled = disabled

def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

# ✅ PRE-HASHED PASSWORDS (tidak hash lagi pas import)
_user1 = User(
    user_id=uuid4(), 
    username="pengguna1", 
    hashed_password="$2b$12$TmJP5appjRpYp0bYUlkzNeT8tDMl5h/Tv39P9dl3hyDruNBqlscUm",
    role="pengguna"
)

_user2 = User(
    user_id=uuid4(), 
    username="peminjam1", 
    hashed_password="$2b$12$IXMHH0mi.lYA.ayNM20.r.0huKOYmlC0ICulcmbbidugK28HLxudu",
    role="peminjam"
)

USERS_DB: Dict[str, User] = {
    _user1.username: _user1,
    _user2.username: _user2,
}

def get_user_by_username(username: str) -> Optional[User]:
    return USERS_DB.get(username)

def get_user_by_id(user_id: str) -> Optional[User]:
    for u in USERS_DB.values():
        if str(u.user_id) == str(user_id):
            return u
    return None