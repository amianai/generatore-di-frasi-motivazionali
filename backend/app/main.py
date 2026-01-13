import random
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_N,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_K,
    FRONTEND_DIR,
    MODEL_PATH,
    MOODS,
)
from .ngram import generate_text, load_model
from .schemas import GenerateRequest, GenerateResponse

app = FastAPI(title="Frasi Motivazionali (n-gram)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

MODEL_STATE = {}


def _load_model() -> None:
    if not MODEL_PATH.exists():
        raise RuntimeError("Model file not found. Run backend/train_model.py")
    state = load_model(MODEL_PATH)
    MODEL_STATE.clear()
    MODEL_STATE.update(state)


@app.on_event("startup")
async def startup_event() -> None:
    _load_model()


@app.get("/")
async def serve_index() -> FileResponse:
    index_path = FRONTEND_DIR / "index.html"
    return FileResponse(index_path)


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/api/moods")
async def moods() -> dict:
    return {
        "moods": [
            {"name": key, "description": value["description"]}
            for key, value in MOODS.items()
        ]
    }


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    if request.mood not in MOODS:
        raise HTTPException(status_code=400, detail="Mood non supportato")
    if not MODEL_STATE:
        raise HTTPException(status_code=500, detail="Modello non caricato")

    mood_data = MOODS[request.mood]
    mood_starter = random.choice(mood_data["starters"])
    seed_parts = [mood_starter]
    if request.seed:
        seed_parts.append(request.seed.strip())
    seed_text = " ".join(seed_parts).strip()
    seed_tokens = seed_text.split() if seed_text else []

    text = generate_text(
        models=MODEL_STATE["models"],
        unigram=MODEL_STATE["unigram"],
        seed_tokens=seed_tokens,
        max_tokens=request.max_tokens,
        n=request.n,
        top_k=request.top_k,
        temperature=request.temperature,
    )

    return GenerateResponse(
        text=text,
        used={
            "mood": request.mood,
            "seed": seed_text,
            "n": request.n,
            "top_k": request.top_k,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        },
    )


def ensure_defaults() -> None:
    """Utility to keep lint/checkers happy in docs."""
    _ = (DEFAULT_N, DEFAULT_TOP_K, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
