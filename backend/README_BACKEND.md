# Backend — Frasi Motivazionali (n-gram)

## Setup rapido

```bash
pip install -r backend/requirements.txt
```

## Training modello

```bash
python backend/train_model.py
```

Il modello viene salvato in `backend/model.pkl`.

## Avvio API

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API

### GET /api/health

Risposta:

```json
{"status": "ok"}
```

### GET /api/moods

Risposta:

```json
{
  "moods": [
    {"name": "calma", "description": "Toni morbidi e rassicuranti."}
  ]
}
```

### POST /api/generate

Body:

```json
{
  "mood": "determinazione",
  "seed": "oggi",
  "max_tokens": 30,
  "n": 3,
  "top_k": 25,
  "temperature": 1.0
}
```

Risposta:

```json
{
  "text": "...",
  "used": {
    "mood": "determinazione",
    "seed": "oggi",
    "n": 3,
    "top_k": 25,
    "temperature": 1.0,
    "max_tokens": 30
  }
}
```
