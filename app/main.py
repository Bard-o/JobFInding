"""
Entry point — orchestrates: authenticate → fetch → store.

Damn if this first iteration was a thing, i cannot imagine the work that this project depares.
"""
# asyncio is a library that allow to run multiple functions at the same time.
# this is called asynchronous programming.
# this is useful for I/O bound tasks like network requests or database queries.
# in this case we are using it for network requests to the Telegram API.
import asyncio

# funtions created earlier and imported from other modules.
from telegram_client import create_client, authenticate, fetch_messages
from database import insert_messages
from config import cfg

# Because our current limiter (specified in telegram_client) is 10, we set the batch size to 10.
# remember to ajust it at your will
BATCH_SIZE = 10


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
