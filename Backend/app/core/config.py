import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

    def __init__(self):
        # Fail fast if configuration is missing!
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is missing in environment variables.")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is missing in environment variables.")
        if not self.ALGORITHM:
            raise ValueError("ALGORITHM is missing in environment variables.")
        if not self.ACCESS_TOKEN_EXPIRE_MINUTES:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES is missing in environment variables.")

settings = Settings()
