import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

APP_TITLE = "AI Data Retrieval Assistant (NL2Pandas)"
TIMEOUT_SECONDS = 10
RESULT_PREVIEW_ROWS = 10
MAX_SAMPLE_ROWS = 3

FORBIDDEN_KEYWORDS = [
    "os", "subprocess", "open", "sys", "shutil",
    "__builtins__", "eval", "exec", "import",
    "getattr", "globals", "locals"
]

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"
GEMINI_API_KEY = os.getenv(GEMINI_API_KEY_ENV)

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please configure it in the .env file.")


def get_gemini_api_key() -> str:
    return os.getenv(GEMINI_API_KEY_ENV, "").strip()