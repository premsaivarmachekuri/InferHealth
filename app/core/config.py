import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "InferHealth"
    VERSION: str = "1.0.0"
    
    # API Keys
    OPEN_AI_KEY: str = os.getenv("OPEN_AI_KEY")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY")
    GEOCODE_API_KEY: str = os.getenv("GEOCODE_API_KEY")
    
    # LLM Settings
    DEFAULT_MODEL: str = "llama-3.1-8b-instant"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    
    # Path Settings
    CHROMA_DB_PATH: str = os.path.join(os.getcwd(), "chroma_db")
    DATA_PATH: str = os.path.join(os.getcwd(), "data")

settings = Settings()
