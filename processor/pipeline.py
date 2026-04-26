"""
Pipeline assembly — builds the full spaCy NLP pipeline with all custom components.

Pipeline order:
    1. es_core_news_sm base (tokenizer, tagger, parser)
    2. EntityRuler (tech term recognition from patterns file)
    3. offer_classifier (rule-based: is this a job offer?)
    4. job_extractor (regex: salary, experience, modality, location, role)

Usage:
    from pipeline import build_pipeline
    nlp = build_pipeline()
    doc = nlp("your text here")
    print(doc.cats["JOB_OFFER"])    # offer score
    print(doc._.job_data)           # extracted fields
"""

import spacy
from components.entity_ruler_setup import add_entity_ruler

# These imports register the components with spaCy via @Language.component
from components.classifier import offer_classifier       # noqa: F401
from components.extractor import job_extractor            # noqa: F401


def build_pipeline() -> spacy.Language:
    """
    Load the Spanish spaCy model and add our custom components.
    Returns a ready-to-use nlp pipeline.
    """
    print("Building spaCy pipeline...")

    # Load base Spanish model (tokenization, POS tagging, NER)
    nlp = spacy.load("es_core_news_sm")

    # Add EntityRuler with tech patterns (placed before NER so our rules take priority)
    add_entity_ruler(nlp)

    # Add our custom classifier (scores how likely the text is a job offer)
    nlp.add_pipe("offer_classifier", last=True)

    # Add our custom extractor (pulls salary, experience, modality, etc.)
    nlp.add_pipe("job_extractor", last=True)

    print(f"✓ Pipeline ready: {nlp.pipe_names}")
    return nlp
