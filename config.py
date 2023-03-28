from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_NAME = getenv("DB_NAME")

    # Keys / authorization
    JWT_KEY = getenv("JWT_KEY")
    ADMIN_KEY = getenv("ADMIN_KEY")

    # Testing
    TESTING = False
