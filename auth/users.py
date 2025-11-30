# auth/users.py
from passlib.context import CryptContext
from uuid import UUID, uuid4
from typing import Optional, Dict

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User:
    def __init__(self, user_id: UUID, username: str, hashed_password: str, role: str, disabled: bool=False):
        self.user_id = user_id
        self.username = username
        self.hashed_password = hashed_password
        self.role = role  # 'pengguna' atau 'peminjam'
        self.disabled = disabled

def hash_password(password: str) -> str:
    # Meng-hash password plaintext
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool: #membandingkan password yang bakal diketik user(plain_password) dengan password yang udah di save di save ke data base (hashed_password)
    return pwd_context.verify(plain_password[:72], hashed_password) #mengecek kecocokan

# Data pengguna (dummy / contoh)
# username: pengguna1 / password: pengguna123  (role: pengguna)
# username: peminjam1 / password: pinjam123     (role: peminjam)
_user1 = User(user_id=uuid4(), username="pengguna1", hashed_password=hash_password("pengguna123"), role="pengguna")
_user2 = User(user_id=uuid4(), username="peminjam1", hashed_password=hash_password("pinjam123"), role="peminjam")

# Disimpan berdasarkan username untuk pencarian cepat
USERS_DB: Dict[str, User] = {
    _user1.username: _user1,
    _user2.username: _user2,
}

def get_user_by_username(username: str) -> Optional[User]:
    # Mengambil user berdasarkan username
    return USERS_DB.get(username)

def get_user_by_id(user_id: str) -> Optional[User]:
    # Mencari user berdasarkan ID
    for u in USERS_DB.values():
        if str(u.user_id) == str(user_id):
            return u
    return None
