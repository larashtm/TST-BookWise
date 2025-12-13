from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

print("pengguna123:", pwd_context.hash("pengguna123"))
print("pinjam123:", pwd_context.hash("pinjam123"))