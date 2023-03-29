from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    DB_HOST = getenv("DB_HOST")
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_USER")
    DB_PASS = getenv("DB_PASS")

    # Keys / authorization
    JWT_KEY = getenv("JWT_KEY")
    ADMIN_KEY = getenv("ADMIN_KEY")

    # Testing
    TESTING = False
