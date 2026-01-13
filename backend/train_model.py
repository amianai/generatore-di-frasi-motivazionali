from app.config import MODEL_PATH, MAX_ARTICLES
from app.data import build_corpus
from app.ngram import build_models, build_unigram, save_model


def main() -> None:
    print(f"Caricamento dataset (max articoli={MAX_ARTICLES})...")
    corpus = build_corpus(MAX_ARTICLES)
    print(f"Frasi raccolte: {len(corpus)}")

    print("Costruzione modelli n-gram...")
    models = build_models(corpus, n_values=[2, 3, 4])
    unigram = build_unigram(corpus)

    save_model(MODEL_PATH, models=models, unigram=unigram)
    print(f"Modello salvato in {MODEL_PATH}")


if __name__ == "__main__":
    main()
