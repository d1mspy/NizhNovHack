from __future__ import annotations
from typing import Iterable, Set, Dict, Any, Tuple
from rapidfuzz import process, fuzz
from .skills_index import get_skill_index

def canonicalize_skills_with_lexicon(
    skills: Iterable[str],
    fuzzy_threshold: int = 90,
) -> Tuple[Set[str], Dict[str, Any]]:
    """
    Возвращает:
      - множество КРАСИВЫХ канонов (как в твоём SKILL_LEXICON: 'Python', 'FastAPI', ...)
      - детали сопоставления {original -> (matched_variant, canonical_display, score)}
    """
    variant2canon, canon_l2disp, variant_list = get_skill_index()
    seen: Set[str] = set()
    details: Dict[str, Any] = {}

    for s in skills or []:
        if not s:
            continue
        orig = s
        sn = " ".join(s.strip().lower().split())

        # 1) прямое попадание по варианту
        if sn in variant2canon:
            canon_l = variant2canon[sn]
            seen.add(canon_l2disp[canon_l])
            details[orig] = {"match_variant": sn, "canonical": canon_l2disp[canon_l], "score": 100}
            continue

        # 2) fuzzy по списку вариантов
        best = process.extractOne(sn, variant_list, scorer=fuzz.token_set_ratio)
        if best and best[1] >= fuzzy_threshold:
            matched_variant = best[0]
            canon_l = variant2canon[matched_variant]
            seen.add(canon_l2disp[canon_l])
            details[orig] = {"match_variant": matched_variant, "canonical": canon_l2disp[canon_l], "score": best[1]}
        else:
            # неизвестный — оставим как есть (как «канон» в красивом виде)
            # чтобы не терять сигнал от редко встречающихся навыков
            seen.add(orig.strip())
            details[orig] = {"match_variant": None, "canonical": orig.strip(), "score": best[1] if best else 0}

    return seen, details
