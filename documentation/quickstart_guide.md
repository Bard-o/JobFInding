# Telegram Job Scraper

Scrape messages from Telegram channels and store them in PostgreSQL. Built with **Telethon**, **Docker**, and **Python**.
the idea is in the future being capable of proscess this data and make dashboards and AI agents to help people find jobs.

> 🚧 Under active development — Iteration 1 (raw message ingestion)

---

## Quick Start

### 1. Get Telegram API credentials

Go to [https://my.telegram.org](https://my.telegram.org) → "API development tools" → create an app to get your `api_id` and `api_hash`.

### 2. Configure environment

```powershell
copy .env.example .env
# Edit .env with your real credentials
```

### 3. Build and run

```powershell
docker compose build
docker compose up db -d                # start Postgres
docker compose run --rm scraper        # run scraper (interactive for first auth)
```

> **First run only:** Telethon will ask for the verification code sent to your Telegram app. After authenticating, the session is saved and future runs are automatic.

### 4. Verify data

```powershell
docker compose exec db psql -U scraper -d telegram_scraper
```

```sql
SELECT COUNT(*) FROM raw_messages;
SELECT telegram_msg_id, message_date, LEFT(text_content, 80)
  FROM raw_messages ORDER BY message_date DESC LIMIT 10;
```

---

## Project Structure

```
JobFinding/
├── .env.example            # env var template (safe to commit)
├── .env                    # real secrets (gitignored)
├── .gitignore
├── docker-compose.yml      # Postgres + Scraper services
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── config.py           # env var loader
│   ├── main.py             # entry point
│   ├── telegram_client.py  # Telethon wrapper
│   └── database.py         # PostgreSQL insertion
├── db/
│   └── init.sql            # auto-runs on first Postgres boot
├── sessions/               # Telethon session file (gitignored)
└── documentation/
```

---

## Local Development

```powershell
cd app
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run Postgres via Docker, scraper locally:

```powershell
docker compose up db -d
# Set POSTGRES_HOST=localhost in .env for local runs
python main.py
```