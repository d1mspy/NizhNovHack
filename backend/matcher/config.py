from dataclasses import dataclass, field

@dataclass(slots=True)
class MatchWeights:
    w_experience: float = 0.5
    w_must: float       = 0.3
    w_nice: float       = 0.1
    w_text: float       = 0.1

@dataclass(slots=True)
class SkillMatchConfig:
    threshold_must: int = 88
    threshold_nice: int = 80
    neutral_must: float = 0.6
    neutral_nice: float = 0.5

@dataclass(slots=True)
class ExperienceConfig:
    under_min_gamma: float = 2.0
    over_max_policy: str   = "cap"   # cap|plateau|bonus
    over_max_bonus: float  = 0.05

@dataclass(slots=True)
class TextSimConfig:
    use_tfidf: bool       = True
    neutral_if_empty: float = 0.5

@dataclass(slots=True)
class MatcherConfig:
    weights: MatchWeights       = field(default_factory=MatchWeights)
    skills: SkillMatchConfig    = field(default_factory=SkillMatchConfig)
    exp: ExperienceConfig       = field(default_factory=ExperienceConfig)
    text: TextSimConfig         = field(default_factory=TextSimConfig)