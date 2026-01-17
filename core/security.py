from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "CHANGE_ME_SECRET"  # потом вынесем в env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def get_password_hash(password: str) -> str:
    """Хешируем пароль"""
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """"Сверяет пароль с хешем"""
    return password_context.verify(password, password_hash)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
