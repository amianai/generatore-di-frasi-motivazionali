import math
import pickle
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

Token = str
Context = Tuple[Token, ...]
NGramCounts = Dict[Context, Dict[Token, int]]


def build_ngram_counts(sentences: Iterable[List[str]], n: int) -> NGramCounts:
    counts: NGramCounts = defaultdict(lambda: defaultdict(int))
    for sentence in sentences:
        tokens = ["<s>"] + sentence + ["</s>"]
        if len(tokens) < n:
            continue
        for i in range(len(tokens) - n + 1):
            context = tuple(tokens[i : i + n - 1])
            next_token = tokens[i + n - 1]
            counts[context][next_token] += 1
    return {context: dict(next_tokens) for context, next_tokens in counts.items()}


def build_models(sentences: Iterable[List[str]], n_values: Iterable[int]) -> Dict[int, NGramCounts]:
    return {n: build_ngram_counts(sentences, n) for n in n_values}


def build_unigram(sentences: Iterable[List[str]]) -> Counter:
    counter: Counter = Counter()
    for sentence in sentences:
        counter.update(sentence)
        counter.update(["</s>"])
    return counter


def save_model(path: Path, models: Dict[int, NGramCounts], unigram: Counter) -> None:
    serializable_models = {
        n: {context: dict(next_tokens) for context, next_tokens in model.items()}
        for n, model in models.items()
    }
    payload = {"models": serializable_models, "unigram": dict(unigram)}
    with path.open("wb") as handle:
        pickle.dump(payload, handle)


def load_model(path: Path) -> Dict[str, object]:
    with path.open("rb") as handle:
        return pickle.load(handle)


def _apply_temperature(weights: Dict[Token, int], temperature: float) -> Dict[Token, float]:
    if temperature <= 0:
        return {token: float(count) for token, count in weights.items()}
    return {token: math.pow(float(count), 1.0 / temperature) for token, count in weights.items()}


def _top_k(weights: Dict[Token, float], k: int) -> Dict[Token, float]:
    if k <= 0 or k >= len(weights):
        return weights
    sorted_items = sorted(weights.items(), key=lambda item: item[1], reverse=True)[:k]
    return dict(sorted_items)


def sample_next(weights: Dict[Token, int], top_k: int, temperature: float) -> Token:
    scaled = _apply_temperature(weights, temperature)
    filtered = _top_k(scaled, top_k)
    tokens = list(filtered.keys())
    probs = list(filtered.values())
    return random.choices(tokens, weights=probs, k=1)[0]


def backoff_context(context: List[Token]) -> Iterable[Context]:
    for start in range(len(context)):
        yield tuple(context[start:])
    yield tuple()


def generate_text(
    models: Dict[int, NGramCounts],
    unigram: Counter,
    seed_tokens: List[str],
    max_tokens: int,
    n: int,
    top_k: int,
    temperature: float,
) -> str:
    tokens = seed_tokens[:]
    for _ in range(max_tokens):
        context_tokens = tokens[-(n - 1) :] if n > 1 else []
        next_weights = None
        for ctx in backoff_context(context_tokens):
            model = models.get(max(len(ctx) + 1, 2))
            if model and ctx in model:
                next_weights = model[ctx]
                break
        if next_weights is None:
            next_weights = {token: int(count) for token, count in unigram.items()}
        next_token = sample_next(next_weights, top_k=top_k, temperature=temperature)
        if next_token == "</s>":
            break
        tokens.append(next_token)
    return " ".join(tokens).strip()
