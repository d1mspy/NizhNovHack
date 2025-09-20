import re
from typing import List, Dict, Tuple, Optional
from rapidfuzz import process, fuzz

from schemas.schemas import ParsedResult
from .patterns.skills import CANONICAL, VARIANTS, SKILL_LEXICON
from .patterns.patterns import SECTION_HINTS, YEARS_PATTERNS, BULLET

def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"[ \t]+", " ", text)

def split_sections(text: str) -> Dict[str, str]:
    sections = {"must": "", "nice": ""}
    lines = text.split("\n")

    def collect(start_idx: int) -> str:
        chunk = []
        for ln in lines[start_idx+1 : min(start_idx+40, len(lines))]:
            # детектор нового заголовка
            if re.match(r"^\s*[A-ZА-Я].{0,30}:\s*$", ln):
                break
            chunk.append(ln)
        return "\n".join(chunk).strip()

    for i, ln in enumerate(lines):
        for pat in SECTION_HINTS["must"]:
            if re.search(pat, ln):
                sections["must"] += "\n" + collect(i)
        for pat in SECTION_HINTS["nice"]:
            if re.search(pat, ln):
                sections["nice"] += "\n" + collect(i)

    if not sections["must"]:
        sections["must"] = "\n".join(lines[:60])
    return sections

def extract_years(text: str) -> Tuple[Optional[int], Optional[int]]:
    mins, maxs = [], []
    for rgx in YEARS_PATTERNS:
        for m in rgx.finditer(text):
            if m.lastindex == 2:
                a, b = int(m.group(1)), int(m.group(2))
                mins.append(min(a, b)); maxs.append(max(a, b))
            elif m.lastindex >= 1:
                val = int(m.group(1))
                mins.append(val)
    if not mins:
        return (None, None)
    return (min(mins), max(maxs) if maxs else None)

def best_skill_match(fragment: str, score_cutoff: int = 88) -> Optional[str]:
    frag = fragment.strip().lower()
    if not frag:
        return None
    match = process.extractOne(frag, CANONICAL, scorer=fuzz.WRatio, score_cutoff=score_cutoff)
    if match:
        return match[0]
    vmatch = process.extractOne(frag, VARIANTS, scorer=fuzz.WRatio, score_cutoff=score_cutoff)
    if not vmatch:
        return None
    variant = vmatch[0].lower()
    for canon, variants in SKILL_LEXICON.items():
        if variant == canon.lower() or variant in [v.lower() for v in variants]:
            return canon
    return None

def extract_skills_block(text: str) -> List[str]:
    items: List[str] = []
    for ln in text.split("\n"):
        if BULLET.match(ln) or len(ln.split()) <= 20:
            items.append(re.sub(BULLET, "", ln).strip())

    candidates = set()
    for it in items:
        # частые шаблоны
        m = re.search(r"(?i)(?:опыт|знание|владение|experience|proficiency|knowledge)\s*(?:работы\s*)?(?:с|в|of|in)\s+(.+)", it)
        parts = []
        if m:
            parts = re.split(r"[,/]|(?:\s+и\s+)|(?:\s+and\s+)|(?:\s+or\s+)", m.group(1))
        else:
            parts = [it]
        for p in parts:
            canon = best_skill_match(p)
            if canon:
                candidates.add(canon)

    return sorted(candidates)

def parse_vacancy_text(text: str) -> ParsedResult:
    text = normalize(text)
    sections = split_sections(text)
    must_txt = sections["must"]
    nice_txt = sections["nice"]

    years_total_min, years_total_max = extract_years(must_txt or text)
    must_skills = extract_skills_block(must_txt)
    nice_skills = extract_skills_block(nice_txt) if nice_txt else []
    nice_skills = [s for s in nice_skills if s not in must_skills]

    return ParsedResult(
        years_total_min=years_total_min,
        years_total_max=years_total_max,
        must_have=must_skills,
        nice_to_have=nice_skills,
    )