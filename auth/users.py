from passlib.context import CryptContext
from uuid import UUID, uuid4
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User:
    def __init__(self, user_id: UUID, username: str, hashed_password: str, disabled: bool=False):
        self.user_id = user_id
        self.username = username
        self.hashed_password = hashed_password
        self.disabled = disabled

# Helper untuk hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# User dummy untuk login
FAKE_USER = User(
    user_id=uuid4(),
    username="alice",
    hashed_password=hash_password("secret123"),
    disabled=False
)

# In-memory database
USERS_DB = {
    "alice": FAKE_USER
}

def get_user(username: str) -> Optional[User]:
    return USERS_DB.get(username)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
