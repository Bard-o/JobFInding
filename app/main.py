"""
Entry point — orchestrates: authenticate → fetch → store.
"""

import asyncio
from telegram_client import create_client, authenticate, fetch_messages
from database import insert_messages
from config import cfg

BATCH_SIZE = 500


async def main():
    client = create_client()

    # 1. Authenticate with Telegram
    await authenticate(client)

    # 2. Fetch messages from the target chat
    messages = await fetch_messages(client, cfg.TELEGRAM_CHAT)

    # 3. Store in PostgreSQL (in batches)
    total_inserted = 0
    for i in range(0, len(messages), BATCH_SIZE):
        batch = messages[i : i + BATCH_SIZE]
        inserted = insert_messages(batch)
        total_inserted += inserted
        print(f"  Batch {i // BATCH_SIZE + 1}: inserted {inserted} rows")

    print(f"✓ Done — {total_inserted} new messages stored in PostgreSQL")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
