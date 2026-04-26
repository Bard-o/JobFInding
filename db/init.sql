-- ══════════════════════════════════════════════════════════════
-- Full database schema for JobFinding
-- This file runs automatically on first Postgres boot via docker-entrypoint-initdb.d
-- ══════════════════════════════════════════════════════════════

-- ── Iteration 1: Raw Telegram messages ──

CREATE TABLE IF NOT EXISTS raw_messages (
    id              SERIAL PRIMARY KEY,
    telegram_msg_id BIGINT NOT NULL,
    chat_id         BIGINT NOT NULL,
    sender_id       BIGINT,
    message_date    TIMESTAMPTZ NOT NULL,
    text_content    TEXT,
    raw_json        JSONB NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (chat_id, telegram_msg_id)
);

-- Index for the most common query: messages from a chat ordered by date
CREATE INDEX IF NOT EXISTS idx_raw_messages_chat_date
    ON raw_messages (chat_id, message_date DESC);


-- ── Iteration 2: Normalized job posting tables ──

-- Lookup table for technology names (e.g. "React", "Docker", "AWS")
CREATE TABLE IF NOT EXISTS technologies (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Structured data extracted from raw messages by the NLP processor
CREATE TABLE IF NOT EXISTS job_posts (
    id               SERIAL PRIMARY KEY,
    message_id       INTEGER NOT NULL REFERENCES raw_messages(id),
    company          VARCHAR(255),
    role             VARCHAR(255),
    modality         VARCHAR(50),       -- 'Remote', 'On-site', 'Hybrid'
    location         VARCHAR(255),
    currency         VARCHAR(10),       -- 'USD', 'COP', etc.
    salary_min       NUMERIC(12, 2),
    salary_max       NUMERIC(12, 2),
    experience_years NUMERIC(4, 1),     -- allows decimals like 1.5
    created_at       TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (message_id)
);

-- Many-to-many relationship: a job post can require multiple technologies
CREATE TABLE IF NOT EXISTS job_post_technologies (
    job_post_id    INTEGER NOT NULL REFERENCES job_posts(id) ON DELETE CASCADE,
    technology_id  INTEGER NOT NULL REFERENCES technologies(id) ON DELETE CASCADE,
    PRIMARY KEY (job_post_id, technology_id)
);
