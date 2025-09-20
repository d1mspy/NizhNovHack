from typing import Dict, Any
from schemas.schemas import UserDTO, VacancyDTO, MatchResult
from .config import MatcherConfig
from .experience import experience_score
from .skills import skills_scores
from .textsim import text_similarity

def compute_match(
    user: UserDTO,
    vacancy: VacancyDTO,
    cfg: MatcherConfig,
    skill_lexicon: Dict[str, list[str]] | None = None
) -> MatchResult:
    # --- 1) опыт ---
    u_months = user.experience_total_months or (user.experience_years * 12 + user.experience_months)
    e = experience_score(
        user_months=u_months,
        min_months=vacancy.min_exp_months,
        max_months=vacancy.max_exp_months,
        gamma=cfg.exp.under_min_gamma,
        over_max_policy=cfg.exp.over_max_policy,
        over_max_bonus=cfg.exp.over_max_bonus,
    )

    # --- 2) скиллы ---
    s_must, s_nice, skill_det = skills_scores(
        user_skills=user.hard_skills,
        must_have=vacancy.must_have,
        nice_to_have=vacancy.nice_to_have,
        threshold_must=cfg.skills.threshold_must,
        threshold_nice=cfg.skills.threshold_nice,
        neutral_must=cfg.skills.neutral_must,
        neutral_nice=cfg.skills.neutral_nice,
    )

    # --- 3) текстовая близость ---
    t = text_similarity(
        user.experience_description or "",
        vacancy.description or "",
        use_tfidf=cfg.text.use_tfidf,
        neutral_if_empty=cfg.text.neutral_if_empty,
    )

    # --- агрегирование ---
    w = cfg.weights
    total = (
        w.w_experience * e +
        w.w_must       * s_must +
        w.w_nice       * s_nice +
        w.w_text       * t
    )
    # в [0..1]
    total = max(0.0, min(1.0, total))

    breakdown = {
        "experience": e,
        "must": s_must,
        "nice": s_nice,
        "text": t,
    }
    details: Dict[str, Any] = {
        "user_months": u_months,
        "vacancy_min": vacancy.min_exp_months,
        "vacancy_max": vacancy.max_exp_months,
        **skill_det
    }
    return MatchResult(total=total, breakdown=breakdown, details=details)
