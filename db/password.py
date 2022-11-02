from passlib.context import CryptContext


password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_ctx.verify(plain_password, hashed_password)


def get_hashed_password(plain_password) -> str:
    return password_ctx.hash(plain_password)