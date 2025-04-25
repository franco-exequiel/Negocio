# config.py
import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()  # Carga el archivo .env en variables de entorno

@dataclass
class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/tienda_db")
    #OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    #WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

settings = Settings()