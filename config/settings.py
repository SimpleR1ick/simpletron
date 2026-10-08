import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Segredos e Configurações
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID_RAW = os.getenv("DISCORD_GUILD_ID", "0")
try:
    GUILD_ID = int(GUILD_ID_RAW)
except ValueError:
    GUILD_ID = 0

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# Diretórios
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

QUOTES_FILE = DATA_DIR / "quotes.json"
GAMES_FILE = DATA_DIR / "games.json"
GIVEAWAYS_FILE = DATA_DIR / "giveaways.json"
WELCOME_FILE = DATA_DIR / "welcome.json"

if not BOT_TOKEN:
    raise ValueError("A variável de ambiente 'DISCORD_BOT_TOKEN' não foi definida no arquivo .env!")
