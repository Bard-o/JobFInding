"""
Rule-based text classifier — determines whether a message is a job offer or noise.

How it works:
    Scans the text for positive signals (keywords/emojis common in job offers)
    and negative signals (patterns common in noise/promos). Produces a score
    between 0.0 and 1.0 stored in doc.cats["JOB_OFFER"].

    The threshold for accepting a message as an offer is configured in config.py
    via the OFFER_THRESHOLD setting (default 0.5).
"""

import re
from spacy.language import Language
from spacy.tokens import Doc


# ══════════════════════════════════════════════════════════════
# POSITIVE SIGNALS — indicators that a message IS a job offer
# Add more keywords here as you discover new patterns!
# ══════════════════════════════════════════════════════════════
POSITIVE_KEYWORDS = [
    # Spanish
    "buscando", "buscamos", "búsqueda", "vacante", "vacantes",
    "experiencia", "requisitos", "modalidad", "salario",
    "contrato", "postúlate", "postularse", "hoja de vida",
    "desarrollador", "ingeniero", "analista", "arquitecto",
    "líder", "senior", "junior", "mid", "practicante",
    # English
    "hiring", "looking for", "vacancy", "requirements",
    "salary", "apply", "opening", "engineer", "developer",
    "experience", "full-time", "part-time", "remote", "internship", "assistant",
]

POSITIVE_EMOJIS = [
    "📍", "💼", "💰", "🚀", "💻", "📧", "📲", "🔹",
    "✅", "🎯", "⚒️", "⚙️", "👩‍💻", "👨‍💻", "🌎",
]

# ══════════════════════════════════════════════════════════════
# NEGATIVE SIGNALS — indicators that a message is noise/promo
# Add more patterns here if you see false positives!
# ══════════════════════════════════════════════════════════════
NEGATIVE_KEYWORDS = [
    "ofertas en:", "follow us", "tag a friend", "sign up",
    "síguenos", "únete a", "join our", "subscribe",
    "newsletter", "descuento", "discount", "promo",
]

# Minimum text length to even consider (very short = probably noise)
MIN_TEXT_LENGTH = 50


@Language.component("offer_classifier")
def offer_classifier(doc: Doc) -> Doc:
    """
    Classify a document as a job offer or noise using keyword scoring.
    Sets doc.cats["JOB_OFFER"] to a float between 0.0 and 1.0.
    """
    text = doc.text
    text_lower = text.lower()

    # If the text is too short, it's almost certainly noise
    if len(text.strip()) < MIN_TEXT_LENGTH:
        doc.cats["JOB_OFFER"] = 0.0
        return doc

    score = 0.0

    # ── Positive scoring ──
    # Each keyword match adds a small amount, capped so one category doesn't dominate
    keyword_hits = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
    score += min(keyword_hits * 0.08, 0.5)  # max +0.5 from keywords

    emoji_hits = sum(1 for em in POSITIVE_EMOJIS if em in text)
    score += min(emoji_hits * 0.06, 0.3)  # max +0.3 from emojis

    # Salary patterns are a very strong signal
    salary_pattern = re.search(
        r"(\$[\d.,]+|\bUSD\b|\bCOP\b|\bsalario\b|\bsalary\b)", text, re.IGNORECASE
    )
    if salary_pattern:
        score += 0.15

    # Experience patterns are also a strong signal
    exp_pattern = re.search(
        r"\d+\+?\s*(años|years|year|año)", text, re.IGNORECASE
    )
    if exp_pattern:
        score += 0.1

    # ── Negative scoring ──
    negative_hits = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)
    score -= negative_hits * 0.15

    # Clamp between 0 and 1
    score = max(0.0, min(1.0, score))

    doc.cats["JOB_OFFER"] = score
    return doc
