"""
Database layer — PostgreSQL connection and message insertion funtions, they'll be used in the main and so.
"""

# these import are drom Dockerfile or the Requirements.txt
import json
import psycopg2
from psycopg2.extras import execute_values
# this import is from config.py, the enviorment variables are stored there as atrivutes.
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
    Insert messages into raw_messages table (check database schema for more info).
    Uses ON CONFLICT DO NOTHING so re-runs are safe (idempotent).
    Returns the count of newly inserted rows.

    Args:
        messages (list[dict]): List of messages to insert. Each message is a dict with the info od the message.
            
    """
    if not messages:
        return 0

    # SQL code to use later, the %s is a placeholder for the values.
    sql = """
        INSERT INTO raw_messages
            (telegram_msg_id, chat_id, sender_id, message_date, text_content, raw_json)
        VALUES %s
        ON CONFLICT (chat_id, telegram_msg_id) DO NOTHING
    """

    # The list argument its a list a dics, here we unpack the values of each dict into a tuple.
    # This is done to make it easier to insert the values into the database (since psycopg2 prefer using tuples).
    # json.dumps convert the metadata dict into a JSON string to put in the raw_json column.
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
                # stores the amount of rows inserted in this batch.
                inserted = cur.rowcount
        return inserted
    finally:
        conn.close()
