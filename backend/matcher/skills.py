# app/matcher/skills.py
from __future__ import annotations
from typing import Iterable, Dict, Any, Tuple
from rapidfuzz import process, fuzz
from .normalization import canonicalize_skills_with_lexicon

def _match_sets(user: set[str], target: set[str], threshold: int) -> tuple[int, int, dict]:
    """
    Для каждого target ищем лучшее соответствие в user (оба уже «красивые» каноны).
    """
    details: dict[str, dict[str, Any]] = {}
    if not target:
        return 0, 0, details

    matched = 0
    u_list = list(user)
    for t in target:
        if not u_list:
            details[t] = {"match": None, "score": 0}
            continue
        best = process.extractOne(t, u_list, scorer=fuzz.token_set_ratio)
        if best and best[1] >= threshold:
            matched += 1
            details[t] = {"match": best[0], "score": best[1]}
        else:
            details[t] = {"match": None, "score": best[1] if best else 0}
    return matched, len(target), details

def skills_scores(
    user_skills: Iterable[str],
    must_have: Iterable[str],
    nice_to_have: Iterable[str],
    threshold_must: int,
    threshold_nice: int,
    neutral_must: float,
    neutral_nice: float,
) -> Tuple[float, float, Dict[str, Any]]:
    # Каноникализация через твой словарь
    u_set, u_det = canonicalize_skills_with_lexicon(user_skills)
    m_set, m_det = canonicalize_skills_with_lexicon(must_have)
    n_set, n_det = canonicalize_skills_with_lexicon(nice_to_have)

    if not m_set:
        must_score = neutral_must
        must_matches = {}
    else:
        m_matched, m_total, must_matches = _match_sets(set(u_set), set(m_set), threshold_must)
        must_score = m_matched / m_total if m_total else neutral_must

    if not n_set:
        nice_score = neutral_nice
        nice_matches = {}
    else:
        n_matched, n_total, nice_matches = _match_sets(set(u_set), set(n_set), threshold_nice)
        nice_score = n_matched / n_total if n_total else neutral_nice

    return must_score, nice_score, {
        "user_canon_skills": sorted(u_set),
        "must_canon": sorted(m_set),
        "nice_canon": sorted(n_set),
        "canonization_details": {
            "user": u_det,
            "must": m_det,
            "nice": n_det,
        },
        "must_matches": must_matches,
        "nice_matches": nice_matches,
    }
