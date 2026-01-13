from collections import Counter

from backend.app.ngram import build_models, build_unigram, generate_text


def test_build_models_and_generate():
    corpus = [["ciao", "mondo"], ["ciao", "amico"]]
    models = build_models(corpus, n_values=[2, 3])
    unigram = build_unigram(corpus)

    assert 2 in models
    assert 3 in models
    assert isinstance(unigram, Counter)

    text = generate_text(
        models=models,
        unigram=unigram,
        seed_tokens=["ciao"],
        max_tokens=5,
        n=2,
        top_k=2,
        temperature=1.0,
    )
    assert text


def test_generate_respects_max_tokens():
    corpus = [["uno", "due", "tre"]]
    models = build_models(corpus, n_values=[2])
    unigram = build_unigram(corpus)

    text = generate_text(
        models=models,
        unigram=unigram,
        seed_tokens=["uno"],
        max_tokens=1,
        n=2,
        top_k=2,
        temperature=1.0,
    )
    assert len(text.split()) <= 2
