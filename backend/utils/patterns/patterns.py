import re

# cекции и маркеры
SECTION_HINTS = {
    "must": [
        r"\bтребовани[ея]\b", r"\bqualifications?\b", r"\brequirements?\b",
        r"\bskills?\b(?!\s*(?:preferred|nice|optional))"
    ],
    "nice": [
        r"\bбудет\s+плюсом\b", r"\bжелательно\b", r"\boptional\b", r"\bnice to have\b",
        r"\bpreferred\b", r"\bwould be a plus\b"
    ],
}
BULLET = re.compile(r"^\s*(?:[-*•▪●]|\d+\.)\s+", re.I)

# поиск общего стажа
YEARS_PATTERNS = [
    re.compile(r"(?i)(?:от|не менее|минимум|min(?:imum)?)\s*(\d+)\s*(?:год(?:а|ов)?|лет|years?)"),
    re.compile(r"(?i)(\d+)\s*[–\-]\s*(\d+)\s*(?:год(?:а|ов)?|лет|years?)"),
    re.compile(r"(?i)(\d+)\s*\+\s*years?"),
    re.compile(r"(?i)(\d+)\s*(?:год(?:а|ов)?|лет|years?)\s*(?:опыта|experience)?"),
]