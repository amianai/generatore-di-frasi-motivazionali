from typing import Dict, Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    mood: str = Field(..., description="Mood selezionato")
    seed: Optional[str] = Field("", description="Seed opzionale dell'utente")
    max_tokens: int = Field(30, ge=5, le=100)
    n: int = Field(3, ge=2, le=4)
    top_k: int = Field(25, ge=0, le=200)
    temperature: float = Field(1.0, ge=0.2, le=2.0)


class GenerateResponse(BaseModel):
    text: str
    used: Dict[str, object]
