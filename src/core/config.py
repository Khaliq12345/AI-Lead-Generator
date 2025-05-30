import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL", "")
TEST_EMAIL = os.getenv("TEST_EMAIL", "")
CLIENT_EMAIL_APP_PASSWORD = os.getenv("CLIENT_EMAIL_APP_PASSWORD", "")
