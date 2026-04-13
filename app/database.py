"""
Database layer — PostgreSQL connection and message insertion.
"""

import json
import psycopg2
from psycopg2.extras import execute_values
from config import cfg


def get_connection():
    """Create and return a new database connection."""
    return psycopg2.connect(
        host=cfg.POSTGRES_HOST,
        port=cfg.POSTGRES_PORT,
        dbname=cfg.POSTGRES_DB,
        user=cfg.POSTGRES_USER,
        password=cfg.POSTGRES_PASSWORD,
    )


def insert_messages(messages: list[dict]) -> int:
    """
    Insert messages into raw_messages table.
    Uses ON CONFLICT DO NOTHING so re-runs are safe (idempotent).
    Returns the count of newly inserted rows.
    """
    if not messages:
        return 0

    sql = """
        INSERT INTO raw_messages
            (telegram_msg_id, chat_id, sender_id, message_date, text_content, raw_json)
        VALUES %s
        ON CONFLICT (chat_id, telegram_msg_id) DO NOTHING
    """

    values = [
        (
            m["telegram_msg_id"],
            m["chat_id"],
            m["sender_id"],
            m["message_date"],
            m["text_content"],
            json.dumps(m["raw_json"]),
        )
        for m in messages
    ]

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                execute_values(cur, sql, values)
                inserted = cur.rowcount
        return inserted
    finally:
        conn.close()
