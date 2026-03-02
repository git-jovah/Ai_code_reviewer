import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Railway will inject these from the "Variables" tab
    GEMINI_API_KEY: str
    MODEL_NAME: str = "gemini-1.5-flash" 
    
    class Config:
        env_file = ".env"

settings = Settings()