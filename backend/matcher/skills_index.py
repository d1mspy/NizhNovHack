from __future__ import annotations
from functools import lru_cache
from typing import Dict, Iterable, Tuple

from utils.patterns.skills import SKILL_LEXICON  # твой файл

def _norm(s: str) -> str:
    # мягкая нормализация — без агрессивных замен типа "javascript"->"js"
    # чтобы не конфликтовать с твоим словарём
    return " ".join(s.strip().lower().split())

@lru_cache(maxsize=1)
def get_skill_index() -> Tuple[Dict[str, str], Dict[str, str], list[str]]:
    """
    Возвращает кортеж:
      - variant2canon_lower: { вариант (lower) -> канон (lower) }
      - canon_lower2display: { канон (lower) -> канон в красивом виде (как в словаре) }
      - variants_list: список всех нормализованных вариантов (для rapidfuzz)
    """
    variant2canon_lower: Dict[str, str] = {}
    canon_lower2display: Dict[str, str] = {}

    for display_canon, variants in SKILL_LEXICON.items():
        canon_l = _norm(display_canon)
        canon_lower2display[canon_l] = display_canon
        # сам канон тоже является вариантом
        variant2canon_lower[canon_l] = canon_l
        for v in variants or ():
            variant2canon_lower[_norm(v)] = canon_l

    variants_list = list(variant2canon_lower.keys())
    return variant2canon_lower, canon_lower2display, variants_list
