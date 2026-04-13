-- Schema for raw Telegram messages (Iteration 1)
-- This file runs automatically on first Postgres boot via docker-entrypoint-initdb.d

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
