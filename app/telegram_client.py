"""
Telegram client wrapper — authentication and message fetching.
"""

import json
from datetime import timezone

from telethon import TelegramClient
from telethon.tl.types import Message
from config import cfg

SESSION_PATH = "sessions/scraper_session"

# ──────────────────────────────────────────────────────────────
# TODO: Change this limit when you're ready to fetch more messages.
#       Set to None to fetch ALL messages from the chat.
# ──────────────────────────────────────────────────────────────
MESSAGE_LIMIT = 100


def create_client() -> TelegramClient:
    """Create a new Telethon client using the stored session."""
    return TelegramClient(
        SESSION_PATH,
        cfg.TELEGRAM_API_ID,
        cfg.TELEGRAM_API_HASH,
    )


async def authenticate(client: TelegramClient) -> None:
    """
    Start the client and authenticate.

    First run:  prompts for the verification code Telegram sends to your phone.
    Later runs: reuses the session file automatically.
    """
    await client.start(phone=cfg.TELEGRAM_PHONE)
    me = await client.get_me()
    print(f"✓ Authenticated as {me.first_name}")


def _serialize_message(msg: Message) -> dict:
    """Convert a Telethon Message into a dict ready for database insertion."""
    return {
        "telegram_msg_id": msg.id,
        "chat_id": msg.chat_id,
        "sender_id": msg.sender_id,
        "message_date": msg.date.astimezone(timezone.utc),
        "text_content": msg.text or "",
        "raw_json": json.loads(msg.to_json()),
    }


async def fetch_messages(client: TelegramClient, chat: str) -> list[dict]:
    """
    Fetch messages from the given chat.

    `chat` can be an invite link (https://t.me/+xxx), a username (@channel),
    or a numeric chat ID.

    Returns a list of dicts ready for insert_messages().
    """
    entity = await client.get_entity(chat)
    messages = []

    async for msg in client.iter_messages(entity, limit=MESSAGE_LIMIT):
        if isinstance(msg, Message):
            messages.append(_serialize_message(msg))

    print(f"✓ Fetched {len(messages)} messages from '{chat}'")
    return messages
