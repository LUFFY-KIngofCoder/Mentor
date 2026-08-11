import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def __init__(self):
        # Fail fast if configuration is missing!
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is missing in environment variables.")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is missing in environment variables.")

settings = Settings()
