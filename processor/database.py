"""
Database layer for the processor — reads raw messages, writes structured job posts.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
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


def fetch_unprocessed_messages() -> list[dict]:
    """
    Fetch raw messages that have NOT been processed into job_posts yet.
    This is done by checking which raw_messages.id values are NOT in job_posts.message_id.
    Only fetches messages that have text content (skips image-only messages).
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT rm.id, rm.text_content
                FROM raw_messages rm
                LEFT JOIN job_posts jp ON rm.id = jp.message_id
                WHERE jp.id IS NULL
                  AND rm.text_content IS NOT NULL
                  AND rm.text_content != ''
                ORDER BY rm.message_date ASC
            """)
            rows = cur.fetchall()
        return rows
    finally:
        conn.close()


def get_or_create_technology(cur, tech_name: str) -> int:
    """
    Look up a technology by name. If it doesn't exist, create it.
    Returns the technology id.
    """
    cur.execute("SELECT id FROM technologies WHERE name = %s", (tech_name,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO technologies (name) VALUES (%s) RETURNING id",
        (tech_name,),
    )
    return cur.fetchone()[0]


def insert_job_post(job_data: dict, message_id: int, tech_names: list[str]) -> int | None:
    """
    Insert a single job post and link its technologies.
    Returns the job_post id, or None if it was a duplicate (already processed).

    Args:
        job_data: dict with keys: role, company, modality, location, currency,
                  salary_min, salary_max, experience_years
        message_id: the raw_messages.id this job post came from
        tech_names: list of normalized technology names (e.g. ["React", "Node.js"])
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # Insert the job post
                cur.execute("""
                    INSERT INTO job_posts
                        (message_id, company, role, modality, location,
                         currency, salary_min, salary_max, experience_years)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (message_id) DO NOTHING
                    RETURNING id
                """, (
                    message_id,
                    job_data.get("company"),
                    job_data.get("role"),
                    job_data.get("modality"),
                    job_data.get("location"),
                    job_data.get("currency"),
                    job_data.get("salary_min"),
                    job_data.get("salary_max"),
                    job_data.get("experience_years"),
                ))

                result = cur.fetchone()
                if result is None:
                    # Already processed (duplicate), skip technologies
                    return None

                job_post_id = result[0]

                # Link technologies via the many-to-many table
                for tech_name in tech_names:
                    tech_id = get_or_create_technology(cur, tech_name)
                    cur.execute("""
                        INSERT INTO job_post_technologies (job_post_id, technology_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                    """, (job_post_id, tech_id))

        return job_post_id
    finally:
        conn.close()
