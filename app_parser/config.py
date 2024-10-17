import os
from dotenv import load_dotenv

load_dotenv()

FASTAPI_API_URL = os.getenv("FASTAPI_API_URL")
