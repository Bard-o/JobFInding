"""
Processor entry point — reads raw messages, runs them through the NLP pipeline,
and stores structured job post data in the database.

Flow:
    1. Fetch unprocessed messages from raw_messages
    2. Build the spaCy pipeline (classifier + entity ruler + extractor)
    3. For each message:
       a. Run through the pipeline
       b. Check classifier score — skip if below threshold
       c. Extract job data + normalized tech names
       d. Insert into job_posts + job_post_technologies
    4. Print summary
"""

from pipeline import build_pipeline
from database import fetch_unprocessed_messages, insert_job_post
from components.normalizer import get_normalized_techs
from config import cfg


def main():
    # 1. Fetch messages that haven't been processed yet
    messages = fetch_unprocessed_messages()
    print(f"Found {len(messages)} unprocessed messages")

    if not messages:
        print("Nothing to process. Done!")
        return

    # 2. Build the NLP pipeline
    nlp = build_pipeline()

    # 3. Process each message
    offers_found = 0
    noise_skipped = 0

    for msg in messages:
        text = msg["text_content"]
        message_id = msg["id"]

        # Run through the spaCy pipeline
        doc = nlp(text)

        # Check classifier score
        offer_score = doc.cats.get("JOB_OFFER", 0.0)

        if offer_score < cfg.OFFER_THRESHOLD:
            noise_skipped += 1
            print(f"  [SKIP] msg #{message_id} — score {offer_score:.2f} (below threshold {cfg.OFFER_THRESHOLD})")
            continue

        # Extract structured data
        job_data = doc._.job_data
        tech_names = get_normalized_techs(doc)

        # Insert into database
        job_post_id = insert_job_post(job_data, message_id, tech_names)

        if job_post_id:
            offers_found += 1
            print(f"  [OK]   msg #{message_id} → job_post #{job_post_id} "
                  f"| score={offer_score:.2f} "
                  f"| role={job_data.get('role', '?')[:50]} "
                  f"| techs={tech_names}")
        else:
            print(f"  [DUP]  msg #{message_id} — already processed")

    # 4. Summary
    print(f"\n{'='*60}")
    print(f"✓ Done — {offers_found} job posts created, {noise_skipped} noise messages skipped")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
