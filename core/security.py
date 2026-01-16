from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Хешируем пароль"""
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """"Сверяет пароль с хешем"""
    return password_context.verify(password, password_hash)
