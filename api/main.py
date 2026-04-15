"""
FastAPI backend — serves messages from the raw_messages table to the React frontend.

Endpoints:
    GET /api/messages?limit=50&offset=0  →  returns a JSON array of messages
"""

import json
import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="JobFinding API")

# Allow the React dev server to call this API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, lock this down to your frontend URL
    allow_methods=["GET"],
    allow_headers=["*"],
)


def get_connection():
    """Create a new database connection using environment variables."""
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "db"),
        port=int(os.environ.get("POSTGRES_PORT", 5432)),
        dbname=os.environ.get("POSTGRES_DB", "telegram_scraper"),
        user=os.environ.get("POSTGRES_USER", "scraper"),
        password=os.environ["POSTGRES_PASSWORD"],
    )


@app.get("/api/messages")
def get_messages(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    """
    Fetch messages from raw_messages, ordered by message_date descending.
    Supports pagination via limit and offset query params.
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    id,
                    telegram_msg_id,
                    chat_id,
                    sender_id,
                    message_date,
                    text_content,
                    created_at
                FROM raw_messages
                ORDER BY message_date DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            rows = cur.fetchall()

        # Convert datetime objects to ISO strings for JSON serialization
        for row in rows:
            row["message_date"] = row["message_date"].isoformat()
            row["created_at"] = row["created_at"].isoformat()

        return rows
    finally:
        conn.close()


@app.get("/api/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
