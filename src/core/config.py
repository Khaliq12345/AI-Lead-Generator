import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
REL_PATH = os.getenv("REL_PATH")
ENV = os.getenv("ENV", "dev")
