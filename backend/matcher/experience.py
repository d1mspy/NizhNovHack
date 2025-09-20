def experience_score(
    user_months: int | None,
    min_months: int | None,
    max_months: int | None,
    gamma: float = 2.0,
    over_max_policy: str = "cap",  # cap|plateau|bonus
    over_max_bonus: float = 0.05
) -> float:
    """
    Нормирует в [0..1] (после обрезки), «режет» недостаток опыта.
    - Если user < min: score = (user/min)^gamma  (жёсткая штрафная кривая).
    - Если min <= user <= max: 1.0
    - Если user > max:
        cap/plateau: 1.0
        bonus: 1.0 + over_max_bonus
    Пустые min/max трактуются как 0 / +inf соответственно.
    """
    if user_months is None:
        return 0.0

    u = max(0, user_months)
    mmin = min_months if min_months is not None else 0
    mmax = max_months  # None -> бесконечность

    if mmax is not None and mmin is not None and mmax < mmin:
        # защитимся от мусора
        mmax = mmin

    if u < mmin:
        if mmin <= 0:
            return 0.0
        raw = (u / mmin) ** gamma
        return max(0.0, min(1.0, raw))
    # внутри окна
    if mmax is None or u <= mmax:
        return 1.0

    # u > max
    if over_max_policy == "bonus":
        return min(1.0, 1.0 + over_max_bonus)
    # 'cap' | 'plateau'
    return 1.0
