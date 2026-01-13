import re
from typing import Iterable, List

from datasets import load_dataset

from .config import DATASET_CONFIG, DATASET_NAME

_SENTENCE_SPLIT = re.compile(r"[.!?]+")
_TOKEN_RE = re.compile(r"[a-zàèéìòù]+|\d+", re.IGNORECASE)


def iter_dataset_text(max_articles: int) -> Iterable[str]:
    dataset = load_dataset(
        DATASET_NAME,
        DATASET_CONFIG,
        split="train",
        streaming=True,
    )
    count = 0
    for row in dataset:
        text = row.get("text", "")
        if text:
            yield text
            count += 1
        if count >= max_articles:
            break


def split_sentences(text: str) -> List[str]:
    cleaned = " ".join(text.split())
    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(cleaned) if s.strip()]
    return sentences


def tokenize_sentence(sentence: str) -> List[str]:
    lowered = sentence.lower()
    return _TOKEN_RE.findall(lowered)


def build_corpus(max_articles: int) -> List[List[str]]:
    corpus: List[List[str]] = []
    for text in iter_dataset_text(max_articles):
        for sentence in split_sentences(text):
            tokens = tokenize_sentence(sentence)
            if tokens:
                corpus.append(tokens)
    return corpus
