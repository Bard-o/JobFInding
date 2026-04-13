"""
Centralized configuration — reads all settings from environment variables.

In Docker: env vars are injected via `env_file: .env` in docker-compose.yml.
Locally:   load them with `python-dotenv` before importing this module,
           or export them in your shell.
"""

import os

# When running locally (outside Docker), load .env automatically
from dotenv import load_dotenv
load_dotenv()


class Config:
    # Telegram
    TELEGRAM_API_ID   = int(os.environ["TELEGRAM_API_ID"])
    TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]
    TELEGRAM_PHONE    = os.environ["TELEGRAM_PHONE"]
    TELEGRAM_CHAT     = os.environ["TELEGRAM_CHAT"]

    # PostgreSQL
    POSTGRES_HOST     = os.environ.get("POSTGRES_HOST", "db")
    POSTGRES_PORT     = int(os.environ.get("POSTGRES_PORT", 5432))
    POSTGRES_DB       = os.environ.get("POSTGRES_DB", "telegram_scraper")
    POSTGRES_USER     = os.environ.get("POSTGRES_USER", "scraper")
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]


cfg = Config()
