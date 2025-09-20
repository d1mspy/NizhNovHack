from typing import Optional

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    _SK_AVAILABLE = True
except Exception:
    _SK_AVAILABLE = False


def text_similarity(
    desc_a: Optional[str],
    desc_b: Optional[str],
    use_tfidf: bool = True,
    neutral_if_empty: float = 0.5
) -> float:
    """
    Возвращает [0..1]. Если один из текстов пуст — нейтральное значение.
    """
    if not desc_a or not desc_b:
        return neutral_if_empty

    if use_tfidf and _SK_AVAILABLE:
        # По умолчанию TF-IDF уже нормализует регистр и токенизирует Unicode-слова.
        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=10000)
        X = vec.fit_transform([desc_a, desc_b])
        sim = cosine_similarity(X[0], X[1])[0, 0]
        return float(sim)

    # Fallback: rapidfuzz без предварительной токенизации
    from rapidfuzz import fuzz
    return fuzz.token_set_ratio(desc_a, desc_b) / 100.0