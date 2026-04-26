"""
Configuration for the processor module — same pattern as the scraper's config.py.
Reads database connection settings from environment variables.
"""

import os

from dotenv import load_dotenv
load_dotenv()


class Config:
    # PostgreSQL
    POSTGRES_HOST     = os.environ.get("POSTGRES_HOST", "db")
    POSTGRES_PORT     = int(os.environ.get("POSTGRES_PORT", 5432))
    POSTGRES_DB       = os.environ.get("POSTGRES_DB", "telegram_scraper")
    POSTGRES_USER     = os.environ.get("POSTGRES_USER", "scraper")
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

    # ──────────────────────────────────────────────────────────
    # CLASSIFIER THRESHOLD
    # Messages scoring BELOW this value are considered noise and
    # will NOT be inserted into job_posts.
    # Raise it to be more strict, lower it to let more through.
    # ──────────────────────────────────────────────────────────
    OFFER_THRESHOLD = float(os.environ.get("OFFER_THRESHOLD", 0.5))


cfg = Config()
