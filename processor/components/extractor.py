"""
Custom spaCy component — extracts structured job data from text using regex.

Extracted fields are stored in doc._.job_data as a dictionary:
    {
        "role": str or None,
        "company": str or None,
        "modality": str or None,      # "Remote", "On-site", "Hybrid"
        "location": str or None,
        "currency": str or None,      # "USD", "COP"
        "salary_min": float or None,
        "salary_max": float or None,
        "experience_years": float or None,
    }
"""

import re
from spacy.language import Language
from spacy.tokens import Doc

# Register the custom extension on Doc objects
if not Doc.has_extension("job_data"):
    Doc.set_extension("job_data", default=None)


# ══════════════════════════════════════════════════════════════
# REGEX PATTERNS for extracting structured data
# ══════════════════════════════════════════════════════════════

# Salary: matches patterns like "$5k-10.8k", "USD $5k-10.8k", "$7.000.000 – $8.000.000"
SALARY_PATTERNS = [
    # USD with "k" notation: "$5k-10.8k", "USD $5k - $10.8k"
    re.compile(
        r"(?:USD\s*)?\$\s*([\d.]+)\s*k\s*[-–—]\s*\$?\s*([\d.]+)\s*k",
        re.IGNORECASE,
    ),
    # COP style with dots as thousands: "$7.000.000 – $8.000.000"
    re.compile(
        r"\$\s*([\d.]+(?:\.\d{3})+)\s*[-–—]\s*\$?\s*([\d.]+(?:\.\d{3})+)",
    ),
    # Single salary with "k": "$5k", "USD $10.8k"
    re.compile(
        r"(?:USD\s*)?\$\s*([\d.]+)\s*k",
        re.IGNORECASE,
    ),
    # Single COP salary: "$7.000.000"
    re.compile(
        r"\$\s*([\d.]+(?:\.\d{3})+)",
    ),
]

# Experience: "3 años de experiencia", "7+ years xp", "al menos 2 años", "más de 4 años"
EXPERIENCE_PATTERNS = [
    re.compile(r"(\d+(?:\.\d+)?)\+?\s*(?:años|año)\s*(?:de\s+experiencia)?", re.IGNORECASE),
    re.compile(r"(?:al\s+menos|mínimo|más\s+de|min(?:imum)?)\s*(\d+(?:\.\d+)?)\s*(?:años|año)", re.IGNORECASE),
    re.compile(r"(\d+)\+?\s*(?:years?)\s*(?:of\s+experience|xp|exp)?", re.IGNORECASE),
]

# Modality keywords → normalized value
MODALITY_MAP = {
    # Spanish
    "100% remoto": "Remote",
    "remoto": "Remote",
    "trabajo remoto": "Remote",
    "full remote": "Remote",
    "remote": "Remote",
    "híbrida": "Hybrid",
    "híbrido": "Hybrid",
    "hibrido": "Hybrid",
    "hibrida": "Hybrid",
    "hybrid": "Hybrid",
    "presencial": "On-site",
    "on-site": "On-site",
    "on site": "On-site",
    "in-office": "On-site",
}

# Location: "en Bogotá", "en Córdoba", "desde Colombia", "Location: Bogotá"
LOCATION_PATTERNS = [
    re.compile(r"(?:📍|ubicación|location)\s*:?\s*(.+?)(?:\n|$)", re.IGNORECASE),
    re.compile(r"(?:en|desde)\s+(bogotá|medellín|cali|barranquilla|cartagena|córdoba|colombia|uruguay|ecuador|brasil|argentina|méxico|paraguay)", re.IGNORECASE),
]

# Currency detection
'''
    I'll add a way to detect the currencie acording to the number lenght
    Beacause the USD salaries are in thousands like 5k 10000 etc
    COP salaries are in millions like 5.000.000 10.000.000 etc
    I think this will work in most cases
'''
CURRENCY_PATTERNS = [
    (re.compile(r"\bUSD\b", re.IGNORECASE), "USD"),
    (re.compile(r"\bCOP\b", re.IGNORECASE), "COP"),
]


def _parse_salary_k(value_str: str) -> float:
    """Convert '5.5' (in k notation) to 5500.0"""
    return float(value_str) * 1000


def _parse_salary_cop(value_str: str) -> float:
    """Convert '7.000.000' (COP dot-separated) to 7000000.0"""
    return float(value_str.replace(".", ""))


def _extract_salary(text: str) -> dict:
    """Extract salary_min, salary_max, and currency from text."""
    result = {"salary_min": None, "salary_max": None, "currency": None}

    # Detect currency
    for pattern, currency in CURRENCY_PATTERNS:
        if pattern.search(text):
            result["currency"] = currency
            break

    # Try each salary pattern in order (most specific first)
    # Pattern 0: USD k-range "$5k-10.8k"
    match = SALARY_PATTERNS[0].search(text)
    if match:
        result["salary_min"] = _parse_salary_k(match.group(1))
        result["salary_max"] = _parse_salary_k(match.group(2))
        if not result["currency"]:
            result["currency"] = "USD"
        return result

    # Pattern 1: COP range "$7.000.000 – $8.000.000"
    match = SALARY_PATTERNS[1].search(text)
    if match:
        result["salary_min"] = _parse_salary_cop(match.group(1))
        result["salary_max"] = _parse_salary_cop(match.group(2))
        if not result["currency"]:
            result["currency"] = "COP"
        return result

    # Pattern 2: Single USD k "$5k"
    match = SALARY_PATTERNS[2].search(text)
    if match:
        result["salary_min"] = _parse_salary_k(match.group(1))
        if not result["currency"]:
            result["currency"] = "USD"
        return result

    # Pattern 3: Single COP "$7.000.000"
    match = SALARY_PATTERNS[3].search(text)
    if match:
        result["salary_min"] = _parse_salary_cop(match.group(1))
        if not result["currency"]:
            result["currency"] = "COP"
        return result

    return result


def _extract_experience(text: str) -> float | None:
    """Extract years of experience as a float. Returns None if not found."""
    for pattern in EXPERIENCE_PATTERNS:
        match = pattern.search(text)
        if match:
            return float(match.group(1))
    return None


def _extract_modality(text: str) -> str | None:
    """Extract work modality. Returns 'Remote', 'On-site', 'Hybrid', or None."""
    text_lower = text.lower()
    # Check longer phrases first to avoid partial matches
    for keyword in sorted(MODALITY_MAP.keys(), key=len, reverse=True):
        if keyword in text_lower:
            return MODALITY_MAP[keyword]
    return None


def _extract_location(text: str) -> str | None:
    """Extract location from text. Returns the first match or None."""
    for pattern in LOCATION_PATTERNS:
        match = pattern.search(text)
        if match:
            location = match.group(1).strip().rstrip(".")
            # Clean up common trailing noise
            if len(location) < 100:  # sanity check
                return location
    return None


def _extract_role(text: str) -> str | None:
    """
    Extract the job role/title from text.
    Heuristic: uses the first substantial non-emoji line as the role.

    NOTE: This is a best-effort heuristic and won't be perfect for all formats.
    It may need improvement in future iterations.
    """
    # Common emoji pattern to strip from beginning of lines
    emoji_pattern = re.compile(
        r"^[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0000FE00-\U0000FEFF"
        r"\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0"
        r"\U0000200D\U0000FE0F\s*\*_]+",
        re.UNICODE,
    )

    for line in text.split("\n"):
        line = line.strip()
        # Strip leading emojis and markdown
        cleaned = emoji_pattern.sub("", line).strip()
        # Skip empty, very short, or URL-only lines
        if len(cleaned) < 10:
            continue
        if cleaned.startswith("http"):
            continue
        if cleaned.startswith("¿") or cleaned.startswith("Hola"):
            continue
        # This is likely the role/title line
        return cleaned[:200]  # cap at 200 chars

    return None


@Language.component("job_extractor")
def job_extractor(doc: Doc) -> Doc:
    """
    Extract structured job data from the document text using regex patterns.
    Stores results in doc._.job_data.
    """
    text = doc.text

    salary_data = _extract_salary(text)

    doc._.job_data = {
        "role": _extract_role(text),
        "company": None,  # hard to extract reliably — left for future iterations
        "modality": _extract_modality(text),
        "location": _extract_location(text),
        "currency": salary_data["currency"],
        "salary_min": salary_data["salary_min"],
        "salary_max": salary_data["salary_max"],
        "experience_years": _extract_experience(text),
    }

    return doc
