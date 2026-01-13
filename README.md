# Frasi Motivazionali (n-gram)

Progetto universitario semplice e completo: backend FastAPI + frontend Vue (via CDN) che genera frasi motivazionali in italiano usando un modello a n-grammi.

## Struttura

```
backend/
  app/
    main.py
    ngram.py
    data.py
    schemas.py
    config.py
  train_model.py
  requirements.txt
  README_BACKEND.md
frontend/
  index.html
  styles.css
  app.js
tests/
  test_ngram.py
  test_api.py
```

## Setup

```bash
pip install -r backend/requirements.txt
```

## Training

Scarica solo un numero limitato di articoli da Wikipedia in italiano (configurato in `backend/app/config.py`).

```bash
python backend/train_model.py
```

Il modello viene salvato in `backend/model.pkl`.

## Avvio

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Apri `http://localhost:8000` per usare l’interfaccia.

## Test

```bash
pytest -q
```

## Scelte progettuali (per l’orale)

- **Interfaccia**: layout minimale con titolo chiaro e controlli essenziali (mood, seed, lunghezza, top-k, temperatura). Serve a rendere esplicite le scelte di generazione e difenderle all’orale.
- **Modello n-gram**: il modello usa l’assunzione di Markov (la prossima parola dipende solo dagli ultimi n-1 token). I conteggi producono una stima MLE delle probabilità di transizione.
- **Sampling**: top-k e temperatura rendono la generazione meno rigida rispetto al greedy. Default scelti (n=3, top-k=25, temperatura=1.0) offrono varietà senza perdere coerenza.
- **Dataset**: Wikipedia italiana è grande, quindi si usa streaming e un numero limitato di articoli; questo rende il training veloce e ripetibile.

## API principali

- `GET /api/health`
- `GET /api/moods`
- `POST /api/generate`

Dettagli in `backend/README_BACKEND.md`.
