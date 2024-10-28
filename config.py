#config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB configuration
    MONGO_URI = os.getenv("MONGO_URI")  # No default value
    DB_NAME = os.getenv("DB_NAME")  # No default value
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")  # No default value

    # Application configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")  # Default can be non-sensitive
    SCRAPER_URL = os.getenv("SCRAPER_URL")  # No default value
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "300000"))

    # Playwright configuration
    PLAYWRIGHT_HEADLESS = os.getenv("PLAYWRIGHT_HEADLESS", "false").lower() in ("true", "1", "t")
    PLAYWRIGHT_SLOW_MO = int(os.getenv("PLAYWRIGHT_SLOW_MO", "2000"))

    # FastAPI configuration
    API_HOST = os.getenv("API_HOST")  
    API_PORT = int(os.getenv("API_PORT", 8080))  

# Instantiate the config object
config = Config()
