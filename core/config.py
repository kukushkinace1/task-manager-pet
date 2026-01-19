from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")# для локал Redis без Docker
# REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/1")
