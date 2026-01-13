from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"
MODEL_PATH = BASE_DIR / "backend" / "model.pkl"

DEFAULT_N = 3
DEFAULT_MAX_TOKENS = 30
DEFAULT_TOP_K = 25
DEFAULT_TEMPERATURE = 1.0

DATASET_NAME = "wikimedia/wikipedia"
DATASET_CONFIG = "20231101.it"
MAX_ARTICLES = 300

MOODS = {
    "calma": {
        "description": "Toni morbidi e rassicuranti.",
        "starters": ["respira", "con pazienza", "un passo alla volta"],
    },
    "determinazione": {
        "description": "Spinta a non mollare e perseverare.",
        "starters": ["oggi decido", "non mollare", "continua a credere"],
    },
    "fiducia": {
        "description": "Fiducia nel processo e nelle proprie capacità.",
        "starters": ["hai già", "puoi farcela", "fidati del processo"],
    },
    "gratitudine": {
        "description": "Riconoscere ciò che si ha e apprezzarlo.",
        "starters": ["ricorda", "apprezza", "sii grato"],
    },
    "energia": {
        "description": "Tono attivo e incoraggiante.",
        "starters": ["vai", "muoviti", "inizia adesso"],
    },
}
