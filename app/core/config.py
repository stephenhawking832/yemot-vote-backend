# app/core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv



# load all the variables found in it as environment variables for our application.
load_dotenv()
# ---------------------------

class Settings(BaseSettings):
    """
    Main settings configuration for the application.
    
    Pydantic's BaseSettings will automatically read from the environment variables.
    Since we already loaded the .env file, Pydantic will find the variables.
    """
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# Create a single, globally accessible instance of the settings.
settings = Settings()